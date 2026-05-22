# nautilus-diff-pdf

Nautilus extension that adds a "Diff PDFs" context menu item when exactly 2 PDF files are selected. Runs `diff-pdf --view` on the selected files.

## Dependencies

- `diff-pdf`
- `gir1.2-nautilus-4.1`
- `python3-nautilus`

## Install

```
make install
nautilus -q && nautilus
```

## Uninstall

```
make uninstall
```
