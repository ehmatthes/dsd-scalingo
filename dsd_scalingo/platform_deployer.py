"""Manages all Scalingo-specific aspects of the deployment process.

Notes:
- 

Add a new file to the user's project, using a template:

    def _add_dockerfile(self):
        # Add a minimal dockerfile.
        template_path = self.templates_path / "dockerfile_example"
        context = {
            "django_project_name": dsd_config.local_project_name,
        }
        contents = plugin_utils.get_template_string(template_path, context)

        # Write file to project.
        path = dsd_config.project_root / "Dockerfile"
        plugin_utils.add_file(path, contents)

Modify user's settings file:

    def _modify_settings(self):
        # Add platformsh-specific settings.
        template_path = self.templates_path / "settings.py"
        context = {
            "deployed_project_name": self._get_deployed_project_name(),
        }
        plugin_utils.modify_settings_file(template_path, context)
"""

import sys, os, re, json
from pathlib import Path
import time

from django.utils.safestring import mark_safe

import requests

from . import deploy_messages as platform_msgs
from .plugin_config import plugin_config

from django_simple_deploy.management.commands.utils import plugin_utils
from django_simple_deploy.management.commands.utils.plugin_utils import dsd_config
from django_simple_deploy.management.commands.utils.command_errors import DSDCommandError


class PlatformDeployer:
    """Perform the initial deployment to Scalingo

    If --automate-all is used, carry out an actual deployment.
    If not, do all configuration work so the user only has to commit changes, and ...
    """

    def __init__(self):
        self.templates_path = Path(__file__).parent / "templates"

    # --- Public methods ---

    def deploy(self, *args, **options):
        """Coordinate the overall configuration and deployment."""
        plugin_utils.write_output("\nConfiguring project for deployment to Scalingo...")

        self._validate_platform()
        self._prep_automate_all()

        # Configure project for deployment to Scalingo
        self._add_python_version()
        self._add_procfile()
        self._add_bin_post_deploy()
        self._add_requirements()
        self._modify_settings()

        self._conclude_automate_all()
        self._show_success_message()

    # --- Helper methods for deploy() ---

    def _validate_platform(self):
        """Make sure the local environment and project supports deployment to Scalingo.

        Returns:
            None
        Raises:
            DSDCommandError: If we find any reason deployment won't work.
        """
        ...


    def _prep_automate_all(self):
        """Take any further actions needed if using automate_all."""
        # DEV: Consider creating these resources as late as possible.
        # Create a new project on Scalingo.
        msg = "  Creating a new app on Scalingo..."
        plugin_utils.write_output(msg)

        # Set the Scalingo project name.
        if not dsd_config.deployed_project_name:
            dsd_config.deployed_project_name = dsd_config.local_project_name
            if len(dsd_config.deployed_project_name) <= 6:
                # Scalingo project names need to be between 6 and 48 characters.
                dsd_config.deployed_project_name += "-deployed"
        
        self.app_name = dsd_config.deployed_project_name

        # Issue CLI command to generate new Scalingo project.
        cmd = f"scalingo create {dsd_config.deployed_project_name}"
        output_obj = plugin_utils.run_quick_command(cmd)
        output_str = output_obj.stdout.decode()
        plugin_utils.write_output(output_str)

        msg = "  Creating a new Postgres db..."
        plugin_utils.write_output(msg)

        cmd = f"scalingo --app {self.app_name} addons-add postgresql postgresql-starter-512"
        output_obj = plugin_utils.run_quick_command(cmd)
        output_str = output_obj.stdout.decode()
        plugin_utils.write_output(output_str)

        # DEV: Write a loop to poll for a running db instance.
        time.sleep(30)

    def _add_python_version(self):
        """Add a .python-version file."""
        path = dsd_config.project_root / ".python-version"
        plugin_utils.add_file(path, contents="3.14")

    def _add_procfile(self):
        """Add a Procfile."""
        path = dsd_config.project_root / "Procfile"
        contents = f"web: gunicorn {dsd_config.local_project_name}.wsgi --log-file -"
        content += "\npostdeploy: bash bin/post_deploy.sh"
        plugin_utils.add_file(path, contents)

    def _add_bin_post_deploy(self):
        """Add a bin/post_deploy.sh file."""
        path_bin = dsd_config.project_root / "bin"
        plugin_utils.add_dir(path_bin)

        path_post_deploy = path_bin / "post_deploy.sh"
        contents = "#!/bin/sh\n\npython manage.py migrate\n"
        plugin_utils.add_file(path_post_deploy, contents)

    def _add_requirements(self):
        """Add requirements for deploying to Scalingo."""
        requirements = ["gunicorn", "psycopg2", "dj-database-url", "whitenoise", "dj-static"]
        plugin_utils.add_packages(requirements)

    def _modify_settings(self):
        # Add Scalingo-specific settings.
        template_path = self.templates_path / "settings.py"
        context = {
            "deployed_project_name": self._get_deployed_project_name(),
        }
        plugin_utils.modify_settings_file(template_path, context)

    def _conclude_automate_all(self):
        """Finish automating the push to Scalingo.

        - Commit all changes.
        - ...
        """
        # Making this check here lets deploy() be cleaner.
        if not dsd_config.automate_all:
            return

        plugin_utils.commit_changes()

        # Push project.
        plugin_utils.write_output("  Deploying to Scalingo...")
        cmd = "git push scalingo main"
        plugin_utils.run_slow_command(cmd)

        # Open project.
        plugin_utils.write_output("  Opening deployed app in a new browser tab...")
        cmd = f"scalingo --apps {self.app_name} open"
        output = plugin_utils.run_quick_command(cmd)
        plugin_utils.write_output(output)

        # Should set self.deployed_url, which will be reported in the success message.
        pass

    def _show_success_message(self):
        """After a successful run, show a message about what to do next.

        Describe ongoing approach of commit, push, migrate.
        """
        if dsd_config.automate_all:
            msg = platform_msgs.success_msg_automate_all(self.deployed_url)
        else:
            msg = platform_msgs.success_msg(log_output=dsd_config.log_output)
        plugin_utils.write_output(msg)
