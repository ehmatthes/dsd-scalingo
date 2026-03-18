"""Tests for Scalingo utils."""

from dsd_scalingo import utils

import sample_output


def test_get_app_names_single_app():
    """Tests for _get_app_names() util function."""
    app_names = utils._get_app_names(sample_output.apps_list_single)
    assert app_names == ["blog-deployed"]

def test_get_app_names_multiple_apps():
    """Tests for get_app_names() util function."""
    app_names = utils._get_app_names(sample_output.apps_list_multiple)
    assert app_names == ["blog-deployed", "blog-2", "blog-3"]

def test_get_app_status():
    """Test for parsing status from apps-info."""
    status = utils._parse_status(sample_output.apps_info_output)
    assert status == "new"