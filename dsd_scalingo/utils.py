"""Utility resources for dsd-scalingo."""

import re

from . import deploy_messages as platform_msgs
from . import key_utils

from django_simple_deploy.management.commands.utils import plugin_utils
from django_simple_deploy.management.commands.utils.command_errors import DSDCommandError


def check_cli_installed():
    """Make sure Scalingo CLI is installed."""
    # DEV: Consider `scalingo self` or `scalingo whoami`
    cmd = "scalingo --version"
    try:
        output_obj = plugin_utils.run_quick_command(cmd)
    except FileNotFoundError:
        raise DSDCommandError(platform_msgs.cli_not_installed)

    if "scalingo version " not in output_obj.stdout.decode():
        raise DSDCommandError(platform_msgs.cli_not_installed)

def check_cli_authenticated():
    """Make sure CLI session is authenticated."""
    cmd = "scalingo whoami"
    output_obj = plugin_utils.run_quick_command(cmd)

    if "You are logged in as " not in output_obj.stdout.decode():
        raise DSDCommandError(platform_msgs.cli_logged_out)


def check_ssh_key_uploaded(key_assist=False):
    """Check that at least one SSH key has been uploaded."""
    cmd = "scalingo keys"
    output_obj = plugin_utils.run_quick_command(cmd)
    output_str = output_obj.stdout.decode().strip()
    if output_str == "┌──────┬─────────┐\n│ NAME │ CONTENT │\n└──────┴─────────┘":
        key_utils.upload_key(key_assist)

def get_new_apps():
    """Check user's apps, and only consider apps that have a status of `new`."""
    cmd = "scalingo apps"
    output_obj = plugin_utils.run_quick_command(cmd)
    app_names = _get_app_names(output_obj.stdout.decode())
    
    return [app for app in app_names if _get_app_status(app) == "new"]

def get_existing_dbs(app_name):
    """Check addons for this Scalingo app, and return any databases."""
    cmd = f"scalingo addons --app {app_name}"
    output_obj = plugin_utils.run_quick_command(cmd)
    return _parse_existing_dbs(output_obj.stdout.decode())


# --- Helper functions ---

def _get_app_names(output_str):
    """Parse output of `scalingo apps` for project names."""
    if "You haven't created any app yet" in output_str:
        return []

    re_app_names = r"^\u2502 (.*?) \u2502"
    matches = re.finditer(re_app_names, output_str, re.MULTILINE)
    matches = [m.group(1).strip() for m in matches]
    matches.remove("NAME")
    return matches

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

def _parse_existing_dbs(addons_info_string):
    """Parse existing databases from result of `addons`."""
    re_dbs = r"^\u2502 PostgreSQL\s*\u2502\s*\S*\s*\u2502 (\S*)\s*\u2502"
    matches = re.finditer(re_dbs, addons_info_string, re.MULTILINE)
    return [m.group(1) for m in matches]