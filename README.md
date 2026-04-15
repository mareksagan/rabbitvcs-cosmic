# rabbitvcs-cosmic

RabbitVCS integration for the COSMIC Files file manager.

## What is this?

This package adds selected [RabbitVCS](https://rabbitvcs.org/) actions directly to the right-click context menu in COSMIC Files. You can choose exactly which actions appear through a simple settings dialog.

When you right-click a file or folder, you will see entries such as:

- Commit
- Diff
- Log
- Revert
- Git Stage / Push / Branches
- SVN Add / Checkout
- ...and whatever else you enable

## Limitations

COSMIC Files does not currently support full file-manager extensions like Nautilus does. Specifically, the following `rabbitvcs-nautilus` features are **not possible** in COSMIC Files at this time:

- **Dynamic conditional menus** based on VCS status (all enabled items are always visible)
- **Submenus** (COSMIC Files ContextActionPreset API is flat only)
- **Status emblems** on file icons
- **Custom list columns** (status, revision, author, age)
- **Properties page** integration

Because of these limitations, only the actions you explicitly enable are added to the context menu. Clicking an action that does not apply to the current selection (for example, clicking *SVN Add* on a Git repository) will let RabbitVCS handle the error, usually with a dialog or no-op.

## Requirements

- COSMIC Files (with ContextActionPreset support)
- RabbitVCS (`rabbitvcs` package)
- Python 3
- `zenity` (optional, for the settings GUI; falls back to GTK3)

## Quick start

```bash
cd rabbitvcs-cosmic
python3 install.py
```

This installs a sensible default set of actions. Then **restart COSMIC Files** (close all windows and reopen) for the menu items to appear.

## Customising which actions appear

Run the settings dialog to pick exactly which actions you want:

```bash
python3 settings.py
```

After changing your selection, re-run `install.py` to update COSMIC Files:

```bash
python3 install.py
```

The configuration is stored in `~/.config/rabbitvcs-cosmic/actions.json`.

## Uninstallation

```bash
python3 uninstall.py
```

## Fallback popup menu

If you prefer a single *RabbitVCS* menu item that opens a popup window instead of a flat list:

```bash
python3 install.py --wrapper ./rabbitvcs-cosmic
```

`rabbitvcs-cosmic` uses `zenity --list` (or a GTK3 fallback) to show the actions in a small dialog.

## System-wide install

```bash
make install PREFIX=/usr/local
python3 install.py --wrapper /usr/local/bin/rabbitvcs-cosmic-action
```

## License

GPL-2.0+ (same as RabbitVCS)
