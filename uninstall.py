#!/usr/bin/env python3
"""Remove the RabbitVCS ContextActionPreset from COSMIC Files configuration."""

import os
import sys

CONFIG_FILE = os.path.expanduser("~/.config/cosmic/com.system76.CosmicFiles/v1/context_actions")


def uninstall():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print(f"Removed {CONFIG_FILE}")
    else:
        print("RabbitVCS context action is not installed.")
    print("Restart COSMIC Files for changes to take effect.")


if __name__ == "__main__":
    uninstall()
