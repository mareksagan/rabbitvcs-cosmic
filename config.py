#!/usr/bin/env python3
"""Configuration management for rabbitvcs-cosmic."""

import json
import os

CONFIG_DIR = os.path.expanduser("~/.config/rabbitvcs-cosmic")
CONFIG_FILE = os.path.join(CONFIG_DIR, "actions.json")

# Each tuple: (display_name, module_name, selection_type, category)
ALL_ACTIONS = [
    # Universal / common
    ("Commit", "commit", "Any", "common"),
    ("Update / Pull", "update", "Any", "common"),
    ("Revert", "revert", "Any", "common"),
    ("Diff", "diff", "Any", "common"),
    ("Show Changes", "show_changes", "Any", "common"),
    ("Compare with Base", "compare_tool", "Any", "common"),
    ("Log", "log", "Any", "common"),
    # SVN specific
    ("SVN Add", "add", "Any", "svn"),
    ("SVN Delete", "delete", "Any", "svn"),
    ("SVN Rename", "rename", "Any", "svn"),
    ("SVN Checkout", "checkout", "Any", "svn"),
    ("SVN Branch/Tag", "branch", "Any", "svn"),
    ("SVN Switch", "switch", "Any", "svn"),
    ("SVN Merge", "merge", "Any", "svn"),
    ("SVN Mark Resolved", "markresolved", "Any", "svn"),
    ("SVN Cleanup", "cleanup", "Any", "svn"),
    # Git specific
    ("Git Stage", "stage", "Any", "git"),
    ("Git Unstage", "unstage", "Any", "git"),
    ("Git Push", "push", "Any", "git"),
    ("Git Branches", "branches", "Any", "git"),
    ("Git Tags", "tags", "Any", "git"),
    ("Git Remotes", "remotes", "Any", "git"),
    ("Git Clone", "clone", "Any", "git"),
    ("Git Reset", "reset", "Any", "git"),
    ("Git Clean", "clean", "Any", "git"),
    # Utilities
    ("Properties", "property_editor", "Any", "utils"),
    ("Settings", "settings", "Any", "utils"),
    ("About", "about", "Any", "utils"),
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
    "Properties",
    "Settings",
}


def load():
    """Load enabled action names from config. Returns set of names."""
    if not os.path.isfile(CONFIG_FILE):
        return set(DEFAULT_ENABLED)
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        enabled = set(data.get("enabled", []))
        if not enabled:
            return set(DEFAULT_ENABLED)
        return enabled
    except (json.JSONDecodeError, OSError):
        return set(DEFAULT_ENABLED)


def save(enabled_names):
    """Save enabled action names to config."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"enabled": sorted(enabled_names)}, f, indent=2)


def get_enabled_actions():
    """Return list of (display_name, module_name, selection_type) for enabled actions."""
    enabled = load()
    return [
        (name, module, selection)
        for name, module, selection, _ in ALL_ACTIONS
        if name in enabled
    ]
