#!/usr/bin/env bash
set -euo pipefail

EXTENSION_DIR="$HOME/.local/share/nautilus-python/extensions"
BASHRC="$HOME/.bashrc"

rm -f "${EXTENSION_DIR}/nautilus-diff-pdf.py"
sed -i '/nautilus-python needs system dist-packages/d' "${BASHRC}"
sed -i '/^export PYTHONPATH="\/usr\/lib\/python3\/dist-packages/d' "${BASHRC}"

echo "Uninstalled."
