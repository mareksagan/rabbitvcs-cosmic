#!/usr/bin/env python3
"""
Interactive settings dialog for rabbitvcs-cosmic.
Lets the user choose which actions appear in the COSMIC Files context menu.
"""

import shutil
import subprocess
import sys

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportError:
    Gtk = None

from config import ALL_ACTIONS, load, save
import install


def run_zenity_settings():
    enabled = load()
    # Build checklist: checkbox state then visible column value per action
    cmd = [
        "zenity",
        "--list",
        "--checklist",
        "--title=RabbitVCS COSMIC Settings",
        "--text=Select actions to show in the COSMIC Files context menu:",
        "--column=",
        "--column=Action",
        "--separator=,",
        "--width=400",
        "--height=600",
    ]
    for name, _, _, _ in ALL_ACTIONS:
        cmd += [str(name in enabled), name]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stderr.strip():
            print(f"Error: {result.stderr.strip()}")
        else:
            print("Cancelled.")
        return

    selected_raw = result.stdout.strip()
    selected = {s.strip() for s in selected_raw.split(",") if s.strip()}
    save(selected)
    print(f"Saved {len(selected)} enabled actions.")
    try:
        install.install(install.find_wrapper())
    except Exception as e:
        print(f"Warning: failed to apply context actions: {e}", file=sys.stderr)


def run_gtk_settings():
    enabled = load()

    window = Gtk.Window(title="RabbitVCS COSMIC Settings")
    window.set_default_size(400, 600)
    window.connect("destroy", Gtk.main_quit)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    window.add(vbox)

    label = Gtk.Label(label="Select actions to show in the COSMIC Files context menu:")
    label.set_margin_top(12)
    label.set_margin_start(12)
    label.set_margin_end(12)
    vbox.pack_start(label, False, False, 0)

    scrolled = Gtk.ScrolledWindow()
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    vbox.pack_start(scrolled, True, True, 0)

    listbox = Gtk.ListBox()
    listbox.set_selection_mode(Gtk.SelectionMode.NONE)
    scrolled.add(listbox)

    checkboxes = {}
    for name, _, _, _ in ALL_ACTIONS:
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_margin_start(12)
        hbox.set_margin_end(12)
        hbox.set_margin_top(6)
        hbox.set_margin_bottom(6)
        row.add(hbox)

        check = Gtk.CheckButton(label=name)
        check.set_active(name in enabled)
        checkboxes[name] = check
        hbox.pack_start(check, True, True, 0)
        listbox.add(row)

    button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    button_box.set_margin_top(12)
    button_box.set_margin_bottom(12)
    button_box.set_margin_start(12)
    button_box.set_margin_end(12)
    button_box.set_homogeneous(True)
    vbox.pack_start(button_box, False, False, 0)

    def on_save(_):
        selected = {name for name, cb in checkboxes.items() if cb.get_active()}
        save(selected)
        print(f"Saved {len(selected)} enabled actions.")
        try:
            install.install(install.find_wrapper())
        except Exception as e:
            print(f"Warning: failed to apply context actions: {e}", file=sys.stderr)
        Gtk.main_quit()

    def on_cancel(_):
        print("Cancelled.")
        Gtk.main_quit()

    save_btn = Gtk.Button(label="Save")
    save_btn.connect("clicked", on_save)
    cancel_btn = Gtk.Button(label="Cancel")
    cancel_btn.connect("clicked", on_cancel)

    button_box.pack_start(cancel_btn, True, True, 0)
    button_box.pack_start(save_btn, True, True, 0)

    window.show_all()
    Gtk.main()


def main():
    if shutil.which("zenity"):
        run_zenity_settings()
    elif Gtk:
        run_gtk_settings()
    else:
        print("Error: neither zenity nor GTK3 (python-gobject) is available.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
