import re, time
import random
import string

import pytest

from tests.e2e_tests.utils import it_helper_functions as it_utils
from . import utils as platform_utils

from tests.e2e_tests.conftest import tmp_project, cli_options


# --- Test functions ---


# For normal test runs, skip this test.
# When working on setup steps, skip other tests and run this one.
#   This will force the tmp_project fixture to run, without doing a full deployment.
@pytest.mark.skip
def test_dummy(tmp_project, request):
    """Helpful to have an empty test to run when testing setup steps."""
    pass


# Skip this test and enable test_dummy() to speed up testing of setup steps.
# @pytest.mark.skip
def test_deployment(tmp_project, cli_options, request):
    """Test the full, live deployment process to Scalingo."""

    # Cache the platform name for teardown work.
    request.config.cache.set("platform", "dsd_scalingo")

    print("\nTesting deployment to Scalingo using the following options:")
    print(cli_options.__dict__)

    python_cmd = it_utils.get_python_exe(tmp_project)

    # Make a unique name for this test deployment, so we can reliably destroy it
    # without risking any of the developer's own projects.
    name_extension = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    app_name = f"blog-e2e-{name_extension}"
    # Cache the app name for teardown work.
    request.config.cache.set("app_name", app_name)

    # Note: If not using automate_all, take steps here that the end user would take.
    # Create a new project on the remote host, if not testing --automate-all.
    if not cli_options.automate_all:
        platform_utils.create_project(app_name)
        request.config.cache.set("app_name", app_name)

    # Run simple_deploy against the test project.
    # We only need to set `--deployed-project-name` for --automate-all. Config-only
    # calls `scalingo create` with the correct name, and the plugin queries for that name.
    if cli_options.automate_all:
        plugin_args_string = f"--deployed-project-name {app_name}"
    else:
        plugin_args_string = ""
    it_utils.run_simple_deploy(python_cmd, automate_all=cli_options.automate_all, plugin_args_string=plugin_args_string)

    # If testing Pipenv, lock after adding new packages.
    if cli_options.pkg_manager == "pipenv":
        it_utils.make_sp_call(f"{python_cmd} -m pipenv lock")

    # For config-only tests, commit changes and run `git push` command.
    if not cli_options.automate_all:
        it_utils.commit_configuration_changes()
        platform_utils.deploy_project(app_name)

    project_url = f"https://{app_name}.osc-fr1.scalingo.io"

    # Remote functionality test often fails if run too quickly after deployment.
    print("\nPausing 10s to let deployment finish...")
    time.sleep(10)

    # Test functionality of both deployed app, and local project.
    #   We want to make sure the deployment works, but also make sure we haven't
    #   affected functionality of the local project using the development server.
    remote_functionality_passed = it_utils.check_deployed_app_functionality(
        python_cmd, project_url
    )
    local_functionality_passed = it_utils.check_local_app_functionality(python_cmd)
    log_check_passed = platform_utils.check_log(tmp_project)

    it_utils.summarize_results(
        remote_functionality_passed,
        local_functionality_passed,
        cli_options,
        tmp_project,
    )

    # Make final assertions, so pytest results are meaningful.
    assert remote_functionality_passed
    assert local_functionality_passed
    assert log_check_passed
