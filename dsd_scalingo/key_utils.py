"""Utilities for managing SSH keys on Scalingo."""

from pathlib import Path

from . import deploy_messages as platform_msgs

from django_simple_deploy.management.commands.utils.plugin_utils import dsd_config
from django_simple_deploy.management.commands.utils import plugin_utils
from django_simple_deploy.management.commands.utils.command_errors import DSDCommandError


def key_assist():
    """Assist with managing SSH keys on Scalingo.

    We only get here if `scalingo keys` returns no existing SSH keys uploaded.
    """
    # Key Assist is not yet available on Windows.
    if dsd_config.on_windows:
        raise DSDCommandError(platform_msgs.no_ssh_keys)

    confirm_assist = plugin_utils.get_confirmation(platform_msgs.key_assist_offer)
    if not confirm_assist:
        raise DSDCommandError(platform_msgs.no_ssh_keys)

    if dsd_config.on_windows:
        plugin_utils.write_output()

    key_paths = _find_keys()

    breakpoint()


def _find_keys():
    """Look for public SSH keys in standard locations.

    Returns: [path_to_key...]
    """
    # Not used now, but don't accidentally look in Windows locations now.
    if dsd_config.on_windows:
        return []

    # Look for ssh-ed25519 public keys.
    path_ssh = Path.home() / ".ssh"
    paths = path_ssh.glob("*.pub")

    # Only keep ssh-ed25519 keys for now.
    key_paths = []
    for p in paths:
        key_text = p.read_text().strip()
        key_type = key_text.split()[0]
        if key_type == "ssh-ed25519":
            key_paths.append(p)

    return key_paths