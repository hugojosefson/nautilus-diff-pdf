# nautilus-diff-pdf

Nautilus extension that adds a "Diff PDFs" context menu item when exactly 2 PDF files are selected. Runs `diff-pdf --view` on the selected files.

## Dependencies

- `diff-pdf`
- `gir1.2-nautilus-4.1` (Ubuntu/Debian) or `nautilus-python` (Fedora)
- `python3-nautilus` (Ubuntu/Debian) or `nautilus-python` (Fedora)

## Install

```bash
git clone https://github.com/user/nautilus-diff-pdf.git
cd nautilus-diff-pdf
bash install.sh
nautilus -q && nautilus
```

Or one-liner:

```bash
bash <(curl -s https://raw.githubusercontent.com/user/nautilus-diff-pdf/main/install.sh)
```

## Uninstall

```bash
bash uninstall.sh
```

## Usage

Select exactly 2 PDF files in Nautilus, right-click, and choose **Diff PDFs**.
