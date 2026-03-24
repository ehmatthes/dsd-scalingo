"""A collection of messages used during the configuration and deployment process."""

# For conventions, see documentation in core deploy_messages.py

from textwrap import dedent

from django.conf import settings


confirm_automate_all = """
The --automate-all flag means django-simple-deploy will:
- Run `scalingo create` for you, to create an empty Scalingo project.
- Run `scalingo --app <app-name> addons-add postgresql postgresql-starter-512`, to create a starter Postgres database.
- Configure your project for deployment on Scalingo.
- Commit all changes to your project that are necessary for deployment.
- Push these changes to Scalingo.
- Open your deployed project in a new browser tab.
"""

cancel_scalingo = """
Okay, cancelling Scalingo configuration and deployment.
"""

# DEV: This could be moved to deploy_messages, with an arg for platform and URL.
cli_not_installed = """
In order to deploy to Scalingo, you need to install the Scalingo CLI.
  See here: https://doc.scalingo.com/tools/cli/start
After installing the CLI, you can run the deploy command again.
"""

cli_logged_out = """
You are currently logged out of the Scalingo CLI. Please log in,
  and then run the deploy command again.
You can log in from  the command line:
  $ scalingo login
"""

# DEV: This should probably be a dynamic string, with the project name.
project_already_exists = """
A remote project with this name already exists.
"""

no_remote_project = """
There is no remote project to deploy to. Before using the configuration-only
mode, please create a remote project. You can use the Scalingo cli to create a
project:
    $ scalingo create <remote-project-name>
"""

multiple_new_apps = """
Multiple apps with a status of `new` were found. There needs to be only one
app with a status of `new` to deploy to.
"""

no_ssh_keys = """
No SSH keys have been uploaded to your Scalingo account.

If you know the path to your public key, you can run:
$ scalingo keys-add <name of key> <path/to/key>

Otherwise, see: https://doc.scalingo.com/platform/getting-started/first-steps#ssh-key-setup
"""


# --- Dynamic strings ---
# These need to be generated in functions, to display information that's determined as
# the script runs.

def use_scalingo_app(app_name):
    """Confirmation message for using a Scalingo app that we found."""
    msg = dedent(
        f"""
        Found one Scalingo app with a status of `new`: {app_name}
        Is this the Scalingo app you want to deploy to?
    """
    )
    return msg

def found_existing_db(app_name, db_names):
    """Confirmation message for using a Scalingo app that we found."""
    db_names = "\n".join(db_names)
    msg = dedent(
        f"""
        The Scalingo app {app_name} already has an existing database:
        {db_names}
        Expecting no database.
    """
    )
    return msg

def success_msg(log_output=""):
    """Success message, for configuration-only run.

    Note: This is immensely helpful; I use it just about every time I do a
      manual test run.
    """

    msg = dedent(
        f"""
        --- Your project is now configured for deployment on Scalingo ---

        To deploy your project, you will need to:
        - Commit the changes made in the configuration process.
            $ git status
            $ git add .
            $ git commit -am "Configured project for deployment."
        - Push your project to Scalingo's servers:
            $ git push scalingo main
        - Open your project:
            $ scalingo open
        - As you develop your project further:
            - Make local changes
            - Commit your local changes
            - Run `git push scalingo main` again to push your changes.
            - Run management commands: `scalingo run python manage.py createsuperuser`
    """
    )

    if log_output:
        msg += dedent(
            f"""
        - You can find a full record of this configuration in the dsd_logs directory.
        """
        )

    return msg


def success_msg_automate_all(deployed_url):
    """Success message, when using --automate-all."""

    msg = dedent(
        f"""

        --- Your project should now be deployed on Scalingo ---

        It should have opened up in a new browser tab. If you see a
          "server not available" message, wait a minute or two and
          refresh the tab. It sometimes takes a few minutes for the
          server to be ready.
        
        - You can also visit your project at {deployed_url}
        - If you make further changes and want to push them to Scalingo,
          commit your changes and then run `git push scalingo main`.
        - Use `scalingo run` to run management commands:
          `scalingo run python manage.py createsuperuser`

    """
    )
    return msg
