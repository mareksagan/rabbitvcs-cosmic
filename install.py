#!/usr/bin/env python3
"""
Install RabbitVCS integration into COSMIC Files.

Generates a ContextActionPreset RON file so that selected RabbitVCS
actions appear directly in the COSMIC Files right-click context menu.
"""

import argparse
import os
import pwd
import shutil
import textwrap

import config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_ACTION = os.path.join(SCRIPT_DIR, "rabbitvcs-cosmic-action")


def find_wrapper():
    if os.path.isfile(LOCAL_ACTION) and os.access(LOCAL_ACTION, os.X_OK):
        return LOCAL_ACTION
    path = shutil.which("rabbitvcs-cosmic-action")
    if path:
        return path
    return LOCAL_ACTION


def _cosmic_config_dir(home_dir):
    return os.path.join(home_dir, ".config", "cosmic", "com.system76.CosmicFiles", "v1")


def install_for_user(wrapper_path, user):
    home_dir = user.pw_dir
    cosmic_config_dir = _cosmic_config_dir(home_dir)
    config_file = os.path.join(cosmic_config_dir, "context_actions")

    # Skip users who have never run COSMIC Files
    if not os.path.isdir(os.path.join(home_dir, ".config", "cosmic")):
        return

    if not os.path.isdir(cosmic_config_dir):
        os.makedirs(cosmic_config_dir, exist_ok=True)
        if os.geteuid() == 0:
            for subdir in (
                os.path.join(home_dir, ".config", "cosmic"),
                os.path.join(home_dir, ".config", "cosmic", "com.system76.CosmicFiles"),
                os.path.join(home_dir, ".config", "cosmic", "com.system76.CosmicFiles", "v1"),
            ):
                if os.path.isdir(subdir):
                    os.chown(subdir, user.pw_uid, user.pw_gid)

    actions = config.get_enabled_actions(home_dir)
    if not actions:
        print(f"Warning: no actions enabled for {user.pw_name}. Run 'python3 settings.py' to select some.")

    lines = ['[']
    for name, module, selection, use_directory in actions:
        dir_flag = " --directory" if use_directory else ""
        entry = textwrap.dedent(f"""\
    (
        name: \"{name}\",
        confirm: false,
        selection: {selection},
        steps: [\"{wrapper_path}{dir_flag} {module} %F\"],
    ),""")
        lines.append(entry)
    lines.append(']')

    content = "\n".join(lines) + "\n"

    with open(config_file, "w") as f:
        f.write(content)

    if os.geteuid() == 0:
        os.chown(config_file, user.pw_uid, user.pw_gid)

    print(f"Installed {len(actions)} RabbitVCS context action(s) for {user.pw_name} to:\n  {config_file}")
    print(f"Using wrapper:\n  {wrapper_path}")


def install(wrapper_path, home_dir=None):
    if home_dir is not None:
        # Look up user info for the provided home directory
        try:
            user = next(u for u in pwd.getpwall() if u.pw_dir == home_dir)
        except StopIteration:
            # Fallback: create a minimal struct-like object
            class _User:
                pass
            user = _User()
            user.pw_dir = home_dir
            user.pw_name = os.path.basename(home_dir) or "user"
            stat = os.stat(home_dir)
            user.pw_uid = stat.st_uid
            user.pw_gid = stat.st_gid
        install_for_user(wrapper_path, user)
        print("Restart COSMIC Files (or open a new window) for changes to take effect.")
        return

    if os.geteuid() == 0:
        for user in pwd.getpwall():
            if user.pw_uid >= 1000 and (
                user.pw_dir.startswith("/home/") or user.pw_dir == "/root"
            ):
                if os.path.isdir(user.pw_dir):
                    install_for_user(wrapper_path, user)
        print("Restart COSMIC Files (or open a new window) for changes to take effect.")
    else:
        user = pwd.getpwuid(os.getuid())
        install_for_user(wrapper_path, user)
        print("Restart COSMIC Files (or open a new window) for changes to take effect.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install rabbitvcs-cosmic into COSMIC Files")
    parser.add_argument(
        "--wrapper",
        default=find_wrapper(),
        help="Path to the rabbitvcs-cosmic-action wrapper script",
    )
    parser.add_argument(
        "--user",
        dest="home_dir",
        default=None,
        help="Home directory of the user to install for (default: current user, or all users if root)",
    )
    args = parser.parse_args()
    install(args.wrapper, args.home_dir)
