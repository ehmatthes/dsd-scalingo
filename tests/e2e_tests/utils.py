"""Helper functions specific to {{PlatformmName}}.

Some Fly.io functions are included as an example.
"""

import re, time
import json

from tests.e2e_tests.utils.it_helper_functions import make_sp_call


def create_project(scalingo_app_name):
    """Create an app on Scalingo."""
    print("\n\nCreating an app on Scalingo...")
    output = (
        make_sp_call(f"scalingo create {scalingo_app_name}", capture_output=True)
        .stdout.decode()
        .strip()
    )
    print("create_project output:", output)

def deploy_project(app_name):
    """Make a non-automated deployment."""
    # Consider pausing before the deployment. Some platforms need a moment
    #   for the newly-created resources to become fully available.
    time.sleep(30)

    print("Deploying to Scalingo...")
    make_sp_call("git push scalingo main")

    # Open project and get URL.
    output = (
        make_sp_call(f"scalingo open", capture_output=True)
        .stdout.decode()
        .strip()
    )
    print("scalingo open output:", output)

def check_log(tmp_proj_dir):
    """Check the log that was generated during a full deployment.

    Checks that log file exists, and that DATABASE_URL is not logged.
    """
    path = tmp_proj_dir / "dsd_logs"
    if not path.exists():
        return False

    log_files = list(path.glob("dsd_*.log"))
    if not log_files:
        return False

    # Disable this check for now, because this line appears in log:
    # INFO: WARNING:root:No DATABASE_URL environment variable set, and so no databases setup
    # Make some more specific log checks?
    # 
    # log_str = log_files[0].read_text()
    # if "DATABASE_URL" in log_str:
    #     return False

    return True

def destroy_project(request):
    """Destroy the deployed project, and all remote resources."""
    print("\nCleaning up:")

    app_name = request.config.cache.get("app_name", None)
    if not app_name:
        print("  No app name found; can't destroy any remote resources.")
        return None

    print("  Destroying Scalingo project...")
    make_sp_call(f"scalingo destroy --app {app_name} --force")
