"""Tests for Scalingo utils."""

from dsd_scalingo import utils

apps_list_single = """
┌───────────────┬───────┬────────┬─────────────────────┐
│     NAME      │ ROLE  │ STATUS │      PROJECT        │
├───────────────┼───────┼────────┼─────────────────────┤
│ blog-deployed │ owner │ new    │ sample_user/default │
└───────────────┴───────┴────────┴─────────────────────┘
"""

apps_list_multiple = """
┌───────────────┬───────┬────────┬─────────────────────┐
│     NAME      │ ROLE  │ STATUS │      PROJECT        │
├───────────────┼───────┼────────┼─────────────────────┤
│ blog-deployed │ owner │ new    │ sample_user/default │
├───────────────┼───────┼────────┼─────────────────────┤
│ blog-2        │ owner │ new    │ sample_user/default │
├───────────────┼───────┼────────┼─────────────────────┤
│ blog-3        │ owner │ new    │ sample_user/default │
└───────────────┴───────┴────────┴─────────────────────┘
"""

apps_info_output = """
┌────────────────┬─────────────────────┐
│    SETTINGS    │       VALUE         │
├────────────────┼─────────────────────┤
│ Project        │ sample_user/default │
│ Force HTTPS    │ false               │
│ Sticky Session │ false               │
│ Stack          │ scalingo-24         │
│ Status         │ new                 │
│ HDS            │ false               │
└────────────────┴─────────────────────┘
"""


def test_get_app_names_single_app():
    """Tests for get_app_names() util function."""
    app_names = utils.get_app_names(apps_list_single)
    assert app_names == ["blog-deployed"]

def test_get_app_names_multiple_apps():
    """Tests for get_app_names() util function."""
    app_names = utils.get_app_names(apps_list_multiple)
    assert app_names == ["blog-deployed", "blog-2", "blog-3"]

def test_get_app_status():
    """Test for parsing status from apps-info."""
    status = utils._parse_status(apps_info_output)
    assert status == "new"