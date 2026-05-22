#!/usr/bin/env bash
set -euo pipefail

EXTENSION_DIR="$HOME/.local/share/nautilus-python/extensions"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASHRC="$HOME/.bashrc"

mkdir -p "${EXTENSION_DIR}"
cp "${SCRIPT_DIR}/nautilus-diff-pdf.py" "${EXTENSION_DIR}/"

if ! grep -qF 'nautilus-python needs system dist-packages' "${BASHRC}"; then
    echo '' >> "${BASHRC}"
    echo '# nautilus-python needs system dist-packages for gi module' >> "${BASHRC}"
    echo 'export PYTHONPATH="/usr/lib/python3/dist-packages${PYTHONPATH:+:$PYTHONPATH}"' >> "${BASHRC}"
fi

echo "Installed. Restart nautilus with: nautilus -q && nautilus"
