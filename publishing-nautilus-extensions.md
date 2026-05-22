# Publishing Nautilus Extensions

## Terminology

The correct term is **"Nautilus extension"** (sometimes "Nautilus plugin" for C extensions). The GitHub topic tag is `nautilus-extension`. Avoid "add-on", "script", or "module" in public-facing documentation.

There are two kinds:

| Type | Extension | Language | Distribution |
| :--- | :--- | :--- | :--- |
| C extension | `.so` shared library compiled from C code | C (GObject/GTK) | System install via Meson/Autotools |
| Python extension | Single `.py` file | Python 3 (PyGObject/GI) | Copy to user or system directory |

Python extensions require the `python3-nautilus` (Debian/Ubuntu) or `nautilus-python` (Fedora/Arch) package.

## Distribution channels

**There is no centralized marketplace for Nautilus extensions.** The [GNOME Extensions website](https://extensions.gnome.org) only supports GNOME Shell extensions, not Nautilus extensions.

Common distribution approaches observed in the wild:

| Channel | Used by | Notes |
| :--- | :--- | :--- |
| GitHub repo | Most Python extensions | README with install instructions |
| Distro packages | Established C extensions (nautilus-admin, etc.) | `apt install nautilus-<name>` |
| AUR (Arch) | Community contributions | `yay -S nautilus-<name>` |
| git.sr.ht | Some developers | Alternative to GitHub |

**No Nautilus extension is published on extensions.gnome.org, PyPI, or Flathub.**

## Build systems

### Python extensions

No build system needed. The extension is a single `.py` file. Distribution is just copying that file to the right location.

### C extensions

- **Meson** (modern, recommended): Used by nautilus-python itself and new projects
- **Autotools** (legacy): Used by older C extensions like nautilus-launch (`configure.ac`, `Makefile.am`, `bootstrap`)

## Installation methods

### Python extensions

Three install locations, checked in this order:

| Path | Scope | Requires root |
| :--- | :--- | :--- |
| `~/.local/share/nautilus-python/extensions/` | Current user only | No |
| `$NAUTILUS_PREFIX/share/nautilus-python/extensions/` | Current user (dev) | No |
| `/usr/share/nautilus-python/extensions/` | All users | Yes |

The **user-local path** (`~/.local/share/nautilus-python/extensions/`) is the standard for most Python extensions.

After installation, restart Nautilus:

```bash
nautilus -q
```

(On Wayland, may need `killall nautilus` or logging out/in.)

### C extensions

System-wide install via Meson:

```bash
meson setup build
meson compile -C build
sudo meson install -C build
```

Shared libraries go to `/usr/lib/x86_64-linux-gnu/nautilus/extensions-4/` (path varies by distro).

### Common installation patterns

Most Python extensions on GitHub use one of:

1. **Manual copy instructions** in README (most common)
2. **Bash install script** (`install.sh`) that copies the file to the right location
3. **curl one-liner** to download directly from raw GitHub:
   ```bash
   mkdir -p ~/.local/share/nautilus-python/extensions
   curl -L -o ~/.local/share/nautilus-python/extensions/extension.py \
     https://raw.githubusercontent.com/user/repo/main/extension.py
   ```

## Project structure conventions

### Python extension (minimal, most common)

```
repo/
├── extension-name.py    # The extension itself
├── README.md            # Instructions + screenshots
├── LICENSE              # MIT, GPL-3.0, etc.
└── install.sh           # Optional: automated install script
```

Examples: [nautilus-open-with-menu](https://github.com/maoschanz/nautilus-open-with-menu), [Nautilus-VSCode](https://github.com/i-am-g2/Nautilus-VSCode)

### Python extension (with install script)

```
repo/
├── extension-name.py
├── README.md
├── LICENSE
├── install.sh           # Copies to ~/.local/share/nautilus-python/extensions/
└── uninstall.sh         # Optional: removes the extension
```

Example: [nautilus-extension-collection](https://github.com/SimBoi/nautilus-extension-collection)

### C extension (Meson)

```
repo/
├── meson.build
├── src/
│   ├── extension.c
│   └── extension.h
├── data/                # Icons, schemas
├── po/                  # Translations
├── README.md
└── COPYING
```

Example: [nautilus-wakatime](https://github.com/fernandoaifer/nautilus-wakatime)

### C extension (Autotools)

```
repo/
├── configure.ac
├── Makefile.am
├── bootstrap
├── src/
│   └── extension.c
├── po/
├── AUTHORS
├── COPYING
├── NEWS
└── ChangeLog
```

Example: [nautilus-launch](https://github.com/madmurphy/nautilus-launch)

## Extension script structure

A Python extension is a single class inheriting from `GObject.GObject` and one or more provider interfaces:

```python
from gi.repository import Nautilus, GObject
from typing import List

class MyExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:
        item = Nautilus.MenuItem(
            name="MyExtension::action",
            label="My Action",
        )
        item.connect("activate", self.on_activate, files)
        return [item]

    def on_activate(self, menu: Nautilus.MenuItem, files: List[Nautilus.FileInfo]):
        pass
```

Provider interfaces available:

| Interface | Purpose |
| :--- | :--- |
| `Nautilus.MenuProvider` | Context menu items |
| `Nautilus.ColumnProvider` | Custom list-view columns |
| `Nautilus.InfoProvider` | File metadata overlay |
| `Nautilus.PropertiesModelProvider` | Properties dialog tabs |

## Distro package naming conventions

Debian/Ubuntu naming pattern: `nautilus-<name>` or `python3-nautilus-<name>` for Python extensions.

Examples from Debian/Ubuntu repos:

- `python3-nautilus` (the nautilus-python framework itself)
- `nautilus-python` (older name, transitional)
- `nautilus-actions` (C extension)
- `nautilus-gsconnect` (C extension)
- `nautilus-image-converter` (C extension)

## Reference extensions

### Python extensions (most relevant for simple menu items)

| Extension | Stars | Approach |
| :--- | :--- | :--- |
| [nautilus-copypath](https://git.sr.ht/~ronenk17/nautilus-copypath) | 52 | Single .py file, curl install |
| [nautilus-extension-collection](https://github.com/SimBoi/nautilus-extension-collection) | 26 | Multiple extensions, install scripts |
| [Nautilus-VSCode](https://github.com/i-am-g2/Nautilus-VSCode) | 14 | install.sh script |
| [nautilus-open-with-menu](https://github.com/maoschanz/nautilus-open-with-menu) | 12 | install.sh + .py file |

### C extensions (for comparison)

| Extension | Stars | Build system |
| :--- | :--- | :--- |
| [nautilus-launch](https://github.com/madmurphy/nautilus-launch) | 12 | Autotools |
| [simple-nautilus-extension](https://github.com/hvoigt/simple-nautilus-extension) | 19 | Makefile (minimal) |

## Recommendations for a simple Python extension

For a Python-based extension with a single menu item (like PDF diff):

### Distribution approach

**GitHub repo with manual copy instructions.** This is the most common, simplest approach for small Python extensions. No build system, no packaging, no distro submission needed.

### Repository structure

```
nautilus-pdf-diff/
├── nautilus-pdf-diff.py   # Extension script
├── README.md              # Usage + install instructions
├── LICENSE                # MIT or GPL-3.0
└── install.sh             # Optional but recommended
```

### Install script template

```bash
#!/usr/bin/env bash
EXTENSION_DIR="$HOME/.local/share/nautilus-python/extensions"
mkdir -p "${EXTENSION_DIR}"
cp "$(dirname "$0")/nautilus-pdf-diff.py" "${EXTENSION_DIR}/"
echo "Installed. Restart Nautilus with: nautilus -q"
```

### README sections

1. Brief description with screenshot
2. Dependencies (`python3-nautilus` / `nautilus-python`)
3. One-line install command (curl or git clone + copy)
4. Uninstall instructions
5. Restart instruction (`nautilus -q`)

### Naming

- GitHub repo: `nautilus-pdf-diff` (kebab-case, `nautilus-` prefix)
- Python file: `nautilus-pdf-diff.py` (matches repo name)
- MenuItem name: `NautilusPdfDiff::compare` (CamelCase namespace)

### What NOT to do

- Don't try to publish on extensions.gnome.org (doesn't support Nautilus)
- Don't publish on PyPI (not discoverable by Nautilus ecosystem)
- Don't use flatpak (Nautilus extensions can't be distributed via flatpak)
- Don't over-engineer with Meson/Autotools (unnecessary for Python extensions)
