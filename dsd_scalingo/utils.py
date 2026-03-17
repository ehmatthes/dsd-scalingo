"""Utility resources for dsd-scalingo."""

import re

from django_simple_deploy.management.commands.utils import plugin_utils


def get_app_names(output_str):
    """Parse output of `scalingo apps` for project names."""
    re_app_names = r"^\u2502 (.*?) \u2502"
    matches = re.finditer(re_app_names, output_str, re.MULTILINE)
    matches = [m.group(1).strip() for m in matches]
    matches.remove("NAME")
    return matches

def get_new_apps(app_names):
    """Check each app, and only keep apps that have a status of `new`."""
    # new_apps = []
    # for app_name in app_names:
    #     status = _get_app_status(app_name)
    #     if status == "new":
    #         new_apps.append(app_name)

    return [app for app in app_names if _get_app_status(app) == "new"]


# --- Helper functions ---

def _get_app_status(app_name):
    """Get the status of a Scalingo app."""
    cmd = f"scalingo apps-info --app {app_name}"
    output_obj = plugin_utils.run_quick_command(cmd)
    return _parse_status(output_obj.stdout.decode())

def _parse_status(apps_info_string):
    """Parse app status from the result of apps-info."""
    re_status = r"^\u2502 Status\s*\u2502\s*(\S*)\s*\u2502"
    m = re.search(re_status, apps_info_string, re.MULTILINE)
    return m.group(1)