# -*- coding: utf-8 -*-

"""Console script for redmine2jira."""

from __future__ import absolute_import

from functools import reduce
from itertools import chain
from operator import and_, itemgetter

import click

from click_default_group import DefaultGroup
from redminelib import Redmine
from redminelib.resultsets import ResourceSet
from six import text_type
from six.moves.urllib.parse import unquote
from tabulate import tabulate

from redmine2jira import config


MISSING_RESOURCE_MAPPINGS_MESSAGE = "Please define missing resource mappings:"
MISSING_RESOURCE_MAPPING_PROMPT_SUFFIX = " -> "


redmine = Redmine(config.REDMINE_URL, key=config.REDMINE_API_KEY)


@click.group(cls=DefaultGroup, default='export', default_if_no_args=True)
def main():
    """
    Export Redmine issues to a set of files which format
    is compatible with the JIRA Importers plugin (JIM).
    """


@main.command('export')
@click.argument('output', type=click.File('w'))
@click.option('--filter', 'query_string',
              help="Filter issues using URL query string syntax. "
                   "Please check documentation for additional details.")
def export_issues(output, query_string):
    """Export Redmine issues."""

    if query_string:
        issues = _get_issues_by_filter(query_string)
    else:
        issues = _get_all_issues()

    click.echo("{:d} issue{} found!"
               .format(len(issues), "s" if len(issues) > 1 else ""))

    # Get all Redmine users and store them by ID
    users = {user.id: user for user in chain(redmine.user.all(),
                                             redmine.user.filter(status=3))}

    groups = None

    if config.ALLOW_ISSUE_ASSIGNMENT_TO_GROUPS:
        # Get all Redmine groups and store them by ID
        groups = {group.id: group for group in redmine.group.all()}

    referenced_users_ids = _export_issues(issues, groups)

    click.echo("Issues exported in '{}'!".format(output.name))

    _list_unmapped_referenced_users(users, referenced_users_ids)

    click.echo()
    click.echo()
    click.echo("Good Bye!")


def _get_issues_by_filter(query_string):
    """
    Fetch issues from Redmine filtering by the parameters
    in a URL query string.

    :param query_string: An URL query string
    :return: Filtered issues
    """
    # Split filters written in URL query string syntax,
    # URL decoding parameters values
    filters = {k: unquote(v)
               for k, v in zip(*[iter([kv for p in query_string.split('&')
                                       for kv in p.split('=')])] * 2)}

    issues = redmine.issue.filter(**filters)

    # The 'issue_id' filter is honored starting from
    # a certain version of Redmine, but it's not known which.
    # If the 'issue_id' filter was in the initial query string,
    # we may need to guess whether it has been ignored or not.
    if 'issue_id' in filters.keys():
        if config.CHECK_ISSUE_ID_FILTER_AVAILABILITY or \
           not config.ISSUE_ID_FILTER_AVAILABLE:
            issues_ids_filter = \
                frozenset(map(int, filters['issue_id'].split(',')))

            # If the total count of the resource set
            # is greater than the number of issue ID's
            # included in the 'issue_id' filter,
            # it means the latter is being ignored...
            if config.CHECK_ISSUE_ID_FILTER_AVAILABILITY:
                click.echo("Checking 'Issue ID' filter availability "
                           "in current Redmine instance...")

            if (config.CHECK_ISSUE_ID_FILTER_AVAILABILITY and
                len(issues) > len(issues_ids_filter)) or \
               not config.ISSUE_ID_FILTER_AVAILABLE:
                if config.CHECK_ISSUE_ID_FILTER_AVAILABILITY:
                    click.echo("The 'Issue ID' filter is not available!")

                    if config.ISSUE_ID_FILTER_AVAILABLE:
                        click.echo("You may disable both the "
                                   "ISSUE_ID_FILTER_AVAILABLE and "
                                   "CHECK_ISSUE_ID_FILTER_AVAILABILITY flags "
                                   "in your settings.")

                # Filter the resource set with the issue ID's in the filter
                issues = [issue for issue in issues
                          if issue.id in issues_ids_filter]

    # FIXME: Debug
    if len(issues) == 1:
        for issue in issues:
            for a, v in list(issue):
                click.echo("{}: {}".format(a, v))

    return issues


def _get_all_issues():
    """
    Fetch all issues from Redmine.

    :return: All issues
    """
    return redmine.issue.all()


def _export_issues(issues, groups):
    """
    Export issues and their relations to a JSON file which structure is
    compatible with the JIRA Importers plugin (JIM).

    All the issue relations which targets are not self-contained in the
    result set are exported in a separate CSV file. Such file should be
    imported whenever all the referenced issues (the endpoints of the
    relations) are already present in the target Jira instance.

    During the export loop all the occurrences of several resource types
    are mapped to Jira resource type instances. The mapping is primarily
    achieved statically, via dictionaries defined in the local configuration
    file by the final user for each resource type; the first time a resource
    misses a static mapping, as a fallback, the final user is prompted to
    interactively specify one, dynamically extending the initial static
    dictionary.

    The resource types that needs a mappings are the following:

    - Users
    - Groups

    Though users references can be found both in the issues properties (author,
    assignee, users related custom fields) and related child resources
    (watchers, attachments, journal entries, time entries), groups references
    can only be found in the "assignee" field.

    :param issues: Issues to export
    :param groups: All Redmine groups
    :return: ID's of users referenced in the issues being exported
    """
    # Get users related issue custom field ID's
    users_related_issue_custom_field_ids = \
        [cf.id for cf in redmine.custom_field.all()
         if cf.customized_type == 'issue' and cf.field_format == 'user']

    referenced_users_ids = set()
    dynamic_mappings_needed = False
    dynamic_groups_mappings = dict()

    for issue in issues:
        # Save author
        referenced_users_ids.add(issue.author.id)

        # If the issue has an assignee...
        if hasattr(issue, 'assigned_to'):
            # Save assignee
            assignee_id = issue.assigned_to.id

            # If the issue assignee is a Redmine group,
            # and the latter has not explicitly mapped to a Jira user...

            if config.ALLOW_ISSUE_ASSIGNMENT_TO_GROUPS and \
               assignee_id in groups:
                group_name = groups[assignee_id].name

                if group_name not in config.CUSTOM_GROUPS_MAPPINGS and \
                   group_name not in dynamic_groups_mappings:
                    if not dynamic_mappings_needed:
                        click.echo(MISSING_RESOURCE_MAPPINGS_MESSAGE)

                        dynamic_mappings_needed = True

                    assignee_jira_username = click.prompt(
                        "[Redmine group name{}Jira username] {}"
                        .format(MISSING_RESOURCE_MAPPING_PROMPT_SUFFIX,
                                group_name),
                        prompt_suffix=MISSING_RESOURCE_MAPPING_PROMPT_SUFFIX)

                    dynamic_groups_mappings[group_name] = \
                        assignee_jira_username

                    # TODO Set value in the final JSON
                    click.echo(assignee_jira_username)
            else:
                referenced_users_ids.add(assignee_id)

        # Save watchers
        for watcher in issue.watchers:
            referenced_users_ids.add(watcher.id)

        # Save attachments
        for attachment in issue.attachments:
            referenced_users_ids.add(attachment.author.id)

        # Save journal entries
        for journal in issue.journals:
            referenced_users_ids.add(journal.user.id)

        # Save time entries
        for time_entry in issue.time_entries:
            referenced_users_ids.add(time_entry.user.id)

        # Save custom fields
        for cf in getattr(issue, 'custom_fields', []):
            if cf.id in users_related_issue_custom_field_ids:
                referenced_users_ids |= \
                    set(cf.value) \
                    if getattr(cf, 'multiple', False) \
                    else {cf.value}

    return referenced_users_ids


def _list_unmapped_referenced_users(users, referenced_users_ids):
    """
    Print in a table fashion all the users not explicitly mapped to specific
    Jira users, via the CUSTOM_USERS_MAPPINGS setting. The purpose is to warn
    the final user to create them in the target Jira instance before importing
    the issues.

    :param users: All Redmine users, including locked ones
    :param referenced_users_ids: ID's of Redmine users referenced
                                 in issues being exported
    """
    # Retrieve all the Redmine users referenced in the issues being
    # exported, excluding the ones that have been explicitly mapped
    # to Jira users.
    # The purpose of this list is to warn the final user to check their
    # existence in the target Jira instance: if the final user willingly
    # mapped a Redmine user to a Jira one obviously we need to exclude
    # it from the list.
    unmapped_referenced_users = \
        [v for k, v in users.items()
         if k in referenced_users_ids and
            v.login not in config.CUSTOM_USERS_MAPPINGS]

    if unmapped_referenced_users:
        click.echo("Loading users referenced in the exported issues...")
        click.echo()

        _list_resources(unmapped_referenced_users,
                        sort_key='login',
                        exclude_attrs=('id',
                                       'created_on',
                                       'last_login_on'))

        click.echo()
        click.echo("No static mappings have been defined for them via the "
                   "CUSTOM_USERS_MAPPINGS setting.")
        click.echo("Ensure the above users already exist in your "
                   "Jira instance before starting the import.")


@main.group('list')
def list_resources():
    """List Redmine resources."""


@list_resources.command('users')
@click.option('--all', 'user_status', flag_value=0,
              help="Get all users")
@click.option('--active', 'user_status', flag_value=1, default=True,
              help="Filter active users")
@click.option('--locked', 'user_status', flag_value=3,
              help="Filter locked users")
def list_users(user_status):
    """List Redmine users."""

    users = None

    if user_status == 0:
        # Get Redmine all users
        users = chain(redmine.user.all(), redmine.user.filter(status=3))
    elif user_status == 1:
        # Get Redmine active users
        users = redmine.user.all()
    elif user_status == 3:
        # Get Redmine locked users
        users = redmine.user.filter(status=3)

    _list_resources(users, sort_key='login', exclude_attrs=('created_on',))


@list_resources.command('groups')
def list_groups():
    """List Redmine groups."""

    groups = redmine.group.all()

    _list_resources(groups, sort_key='name')


@list_resources.command('projects')
def list_projects():
    """List Redmine projects."""

    projects = redmine.project.all()

    def get_project_full_name(project, full_name):
        """
        Build the full name of the project including hierarchy information.

        :param project: Project Resource
        :param full_name: Full name of the project used in the recursion
        :return: Project full name (at the end of recursion)
        """
        # If it's not the first level of recursion...
        if full_name != project.name:
            full_name = "{} / {}".format(project.name, full_name)
        else:
            full_name = project.name

        if hasattr(project, 'parent'):
            parent = redmine.project.get(project.parent.id)
            full_name = get_project_full_name(parent, full_name)

        return full_name

    _list_resources(projects,
                    sort_key='name',
                    format_dict={'name': get_project_full_name},
                    exclude_attrs=('description', 'enabled_modules',
                                   'created_on', 'updated_on'))


@list_resources.command('trackers')
def list_trackers():
    """List Redmine trackers."""

    trackers = redmine.tracker.all()

    _list_resources(trackers,
                    sort_key='name',
                    exclude_attrs={'default_status': lambda r, v: v.name})


@list_resources.command('queries')
def list_queries():
    """List Redmine queries."""

    queries = redmine.query.all()

    _list_resources(queries, sort_key='name')


@list_resources.command('issue_statuses')
def list_issues_statuses():
    """List Redmine issue statuses."""

    issue_statuses = redmine.issue_status.all()

    _list_resources(issue_statuses, sort_key='name')


@list_resources.command('custom_fields')
def list_custom_fields():
    """List Redmine custom fields."""

    custom_fields = redmine.custom_field.all()

    _list_resources(custom_fields, sort_key='name')


def _list_resources(resource_set, sort_key,
                    format_dict=None, exclude_attrs=None):
    # Find resource attributes excluding relations with other resource types
    scalar_attributes = \
        (set((a for a in dir(resource)
              if not isinstance(getattr(resource, a), ResourceSet)))
         for resource in resource_set)

    # Compute a common subset among all the scalar attributes
    common_scalar_attributes = reduce(and_, scalar_attributes)
    # Declare base headers for all resource types
    base_headers = ['id']

    # Exclude specific attributes
    if exclude_attrs:
        base_headers[:] = [h for h in base_headers if h not in exclude_attrs]
        common_scalar_attributes -= set(exclude_attrs)

    # Appending sorting key to base headers
    if sort_key not in base_headers:
        base_headers.append(sort_key)

    # Create table headers appending lexicographically sorted
    # common attribute names to base headers list, which has
    # already been statically ordered.
    headers = \
        base_headers + sorted(common_scalar_attributes - set(base_headers))

    def _format(key, resource):
        value = getattr(resource, key)

        if format_dict and key in format_dict:
            return format_dict[key](resource, value)

        return text_type(value)

    # Build a "table" (list of dictionaries)
    # from all the resource instances,
    # using only the calculated attributes
    resource_table = sorted(({h: _format(h, resource) for h in headers}
                             for resource in resource_set),
                            key=itemgetter(sort_key))

    # Pretty print the resource table
    # using the dictionary keys as headers
    click.echo(tabulate(resource_table, headers="keys"))
