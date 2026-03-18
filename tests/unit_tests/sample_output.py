"""Sample Scalingo cli output for unit tests."""

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

addons_empty = """
┌───────┬────┬──────┬────────┐
│ ADDON │ ID │ PLAN │ STATUS │
└───────┴────┴──────┴────────┘
"""