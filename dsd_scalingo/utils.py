"""Utility resources for dsd-scalingo."""

import re


def get_app_names(output_str):
    """Parse output of `scalingo apps` for project names."""
    re_app_names = r"^\u2502 (.*?) \u2502"
    matches = re.finditer(re_app_names, output_str, re.MULTILINE)
    matches = [m.group(1).strip() for m in matches]
    matches.remove("NAME")
    return matches
