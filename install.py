#!/usr/bin/env python3
"""
Install RabbitVCS integration into COSMIC Files.

Generates a ContextActionPreset RON file so that selected RabbitVCS
actions appear directly in the COSMIC Files right-click context menu.
"""

import argparse
import os
import shutil
import textwrap

import config

CONFIG_DIR = os.path.expanduser("~/.config/cosmic/com.system76.CosmicFiles/v1")
CONFIG_FILE = os.path.join(CONFIG_DIR, "context_actions")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_ACTION = os.path.join(SCRIPT_DIR, "rabbitvcs-cosmic-action")


def find_wrapper():
    if os.path.isfile(LOCAL_ACTION) and os.access(LOCAL_ACTION, os.X_OK):
        return LOCAL_ACTION
    path = shutil.which("rabbitvcs-cosmic-action")
    if path:
        return path
    return LOCAL_ACTION


def install(wrapper_path):
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

    actions = config.get_enabled_actions()
    if not actions:
        print("Warning: no actions are enabled. Run 'python3 settings.py' to select some.")

    lines = ['[']
    for name, module, selection in actions:
        entry = textwrap.dedent(f"""\
    (
        name: \"{name}\",
        confirm: false,
        selection: {selection},
        steps: [\"{wrapper_path} {module} %F\"],
    ),""")
        lines.append(entry)
    lines.append(']')

    content = "\n".join(lines) + "\n"

    with open(CONFIG_FILE, "w") as f:
        f.write(content)

    print(f"Installed {len(actions)} RabbitVCS context action(s) to:\n  {CONFIG_FILE}")
    print(f"Using wrapper:\n  {wrapper_path}")
    print("Restart COSMIC Files (or open a new window) for changes to take effect.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install rabbitvcs-cosmic into COSMIC Files")
    parser.add_argument(
        "--wrapper",
        default=find_wrapper(),
        help="Path to the rabbitvcs-cosmic-action wrapper script",
    )
    args = parser.parse_args()
    install(args.wrapper)
