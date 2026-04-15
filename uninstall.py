#!/usr/bin/env python3
"""Remove the RabbitVCS ContextActionPreset from COSMIC Files configuration."""

import os
import pwd

CONFIG_PATH = ".config/cosmic/com.system76.CosmicFiles/v1/context_actions"


def uninstall_for_user(home_dir):
    config_file = os.path.join(home_dir, CONFIG_PATH)
    if os.path.exists(config_file):
        os.remove(config_file)
        print(f"Removed {config_file}")


def uninstall():
    if os.geteuid() == 0:
        # Running as root: remove for all regular users
        for user in pwd.getpwall():
            if user.pw_uid >= 1000 and (
                user.pw_dir.startswith("/home/") or user.pw_dir == "/root"
            ):
                uninstall_for_user(user.pw_dir)
        # Also check root explicitly in case root has a different uid
        uninstall_for_user("/root")
    else:
        uninstall_for_user(os.path.expanduser("~"))

    print("Restart COSMIC Files for changes to take effect.")


if __name__ == "__main__":
    uninstall()
