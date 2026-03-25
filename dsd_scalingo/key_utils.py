"""Utilities for managing SSH keys on Scalingo."""

from . import deploy_messages as platform_msgs

from django_simple_deploy.management.commands.utils import plugin_utils
from django_simple_deploy.management.commands.utils.command_errors import DSDCommandError


def key_assist():
    """Assist with managing SSH keys on Scalingo.

    We only get here if `scalingo keys` returns no existing SSH keys uploaded.
    """
    confirm_assist = plugin_utils.get_confirmation(platform_msgs.key_assist_offer)
    if not confirm_assist:
        raise DSDCommandError(platform_msgs.no_ssh_keys)



    breakpoint()