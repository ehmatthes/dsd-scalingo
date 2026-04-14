"""Utilities for managing SSH keys on Scalingo."""

from pathlib import Path
import socket

from . import deploy_messages as platform_msgs

from django_simple_deploy.management.commands.utils.plugin_utils import dsd_config
from django_simple_deploy.management.commands.utils import plugin_utils
from django_simple_deploy.management.commands.utils.command_errors import DSDCommandError


def upload_key(key_assist=False):
    """Assist with managing SSH keys on Scalingo.

    We only get here if `scalingo keys` returns no existing SSH keys uploaded.
    """
    # Remove this block when the --key-assist feature flag is removed.
    if not key_assist:
        raise DSDCommandError(platform_msgs.no_ssh_keys)

    # Key Assist is not yet available on Windows.
    if dsd_config.on_windows:
        msg = "Key assistance is not yet supported on Windows."
        plugin_utils.write_output(msg)
        raise DSDCommandError(platform_msgs.no_ssh_keys)

    # Verify the user wants assistance with managing keys.
    confirm_assist = plugin_utils.get_confirmation(platform_msgs.key_assist_offer)
    if not confirm_assist:
        raise DSDCommandError(platform_msgs.no_ssh_keys)

    key_paths = _find_keys()

    if not key_paths:
        # No suitable keys found.
        msg = "No suitable SSH keys were found. Support for generating new keys is not implemented yet."
        plugin_utils.write_output(msg)
        raise DSDCommandError(platform_msgs.no_ssh_keys)

    elif len(key_paths) == 1:
        # One key found. Ask if it's okay to use.
        # DEV: If not, offer to generate a new pair when that's supported.
        key_path = key_paths[0]
        msg = f"One public SSH key found: {key_path.as_posix()}"
        msg += "\nWould you like to upload this key?\n"
        confirm_upload_key = plugin_utils.get_confirmation(msg)

        if confirm_upload_key:
            suggested_name = _get_suggested_key_name()
            msg = f"Okay to use key name: {suggested_name}\n"
            confirm_suggested_name = plugin_utils.get_confirmation(msg)
            if not confirm_suggested_name:
                msg = "Support for using a custom key name not implemented yet."
                plugin_utils.write_output(msg)
                raise DSDCommandError(platform_msgs.no_ssh_keys)

            cmd = f"scalingo keys-add {suggested_name} {key_path.as_posix()}"
            output_obj = plugin_utils.run_quick_command(cmd)
            plugin_utils.write_output(output_obj)
            return

        else:
            raise DSDCommandError(platform_msgs.no_ssh_keys)

    else:
        # More than one key found. Ask which to use.
        msg = "Multiple SSH keys were found. Support for choosing a key is not implemented yet."
        plugin_utils.write_output(msg)
        raise DSDCommandError(platform_msgs.no_ssh_keys)


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

def _get_suggested_key_name():
    """Return a suitable name for the SSH key we're about to upload."""
    hostname = socket.gethostname().replace(".local", "")
    return f"dsd-scalingo-{hostname}"
