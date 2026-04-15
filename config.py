#!/usr/bin/env python3
"""Configuration management for rabbitvcs-cosmic."""

import json
import os


def _config_dir(home_dir=None):
    if home_dir is None:
        home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".config", "rabbitvcs-cosmic")


def _config_file(home_dir=None):
    return os.path.join(_config_dir(home_dir), "actions.json")


# Each tuple: (display_name, module_name, selection_type, category, use_directory)
ALL_ACTIONS = [
    # Universal / common
    ("Commit", "commit", "Any", "common", True),
    ("Update / Pull", "update", "Any", "common", True),
    ("Revert", "revert", "Any", "common", True),
    ("Diff", "diff", "Any", "common", False),
    ("Show Changes", "show_changes", "Any", "common", False),
    ("Compare with Base", "compare_tool", "Any", "common", False),
    ("Log", "log", "Any", "common", True),
    # SVN specific
    ("SVN Add", "add", "Any", "svn", True),
    ("SVN Delete", "delete", "Any", "svn", False),
    ("SVN Rename", "rename", "Any", "svn", False),
    ("SVN Checkout", "checkout", "Any", "svn", True),
    ("SVN Branch/Tag", "branch", "Any", "svn", True),
    ("SVN Switch", "switch", "Any", "svn", True),
    ("SVN Merge", "merge", "Any", "svn", True),
    ("SVN Mark Resolved", "markresolved", "Any", "svn", False),
    ("SVN Cleanup", "cleanup", "Any", "svn", True),
    # Git specific
    ("Git Stage", "stage", "Any", "git", True),
    ("Git Unstage", "unstage", "Any", "git", True),
    ("Git Push", "push", "Any", "git", True),
    ("Git Branches", "branches", "Any", "git", True),
    ("Git Tags", "tags", "Any", "git", True),
    ("Git Remotes", "remotes", "Any", "git", True),
    ("Git Clone", "clone", "Any", "git", True),
    ("Git Reset", "reset", "Any", "git", True),
    ("Git Clean", "clean", "Any", "git", True),
    # Utilities
    ("Properties", "property_editor", "Any", "utils", False),
    ("Settings", "settings", "Any", "utils", True),
    ("About", "about", "Any", "utils", True),
]

# Sensible default set
DEFAULT_ENABLED = {
    "Commit",
    "Update / Pull",
    "Revert",
    "Diff",
    "Log",
    "Git Stage",
    "Git Push",
    "Git Branches",
    "SVN Add",
    "SVN Checkout",
    "Git Clone",
    "Properties",
    "Settings",
}


def load(home_dir=None):
    """Load enabled action names from config. Returns set of names."""
    config_file = _config_file(home_dir)
    if not os.path.isfile(config_file):
        return set(DEFAULT_ENABLED)
    try:
        with open(config_file, "r") as f:
            data = json.load(f)
        enabled = set(data.get("enabled", []))
        if not enabled:
            return set(DEFAULT_ENABLED)
        return enabled
    except (json.JSONDecodeError, OSError):
        return set(DEFAULT_ENABLED)


def save(enabled_names, home_dir=None):
    """Save enabled action names to config."""
    config_dir = _config_dir(home_dir)
    os.makedirs(config_dir, exist_ok=True)
    config_file = _config_file(home_dir)
    with open(config_file, "w") as f:
        json.dump({"enabled": sorted(enabled_names)}, f, indent=2)


def get_enabled_actions(home_dir=None):
    """Return list of (display_name, module_name, selection_type, use_directory) for enabled actions."""
    enabled = load(home_dir)
    return [
        (name, module, selection, use_directory)
        for name, module, selection, _, use_directory in ALL_ACTIONS
        if name in enabled
    ]
