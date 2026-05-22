# nautilus-diff-pdf

Nautilus extension that adds a "Diff PDFs" context menu item when exactly 2 PDF files are selected. Runs [`diff-pdf`](https://vslavik.github.io/diff-pdf/) `--view` on the selected files.

## Dependencies

- [`diff-pdf`](https://vslavik.github.io/diff-pdf/) — e.g. [`diff-pdf-wx`](https://packages.ubuntu.com/search?keywords=diff-pdf) on Ubuntu
- `gir1.2-nautilus-4.1` (Ubuntu/Debian) or `nautilus-python` (Fedora)
- `python3-nautilus` (Ubuntu/Debian) or `nautilus-python` (Fedora)

Install all at once:

```bash
sudo apt install -y diff-pdf-wx gir1.2-nautilus-4.1 python3-nautilus
```

## Install

```bash
mkdir -p ~/.local/share/nautilus-python/extensions
curl -sL https://raw.githubusercontent.com/user/nautilus-diff-pdf/main/nautilus-diff-pdf.py \
  -o ~/.local/share/nautilus-python/extensions/nautilus-diff-pdf.py
```

Then restart Nautilus: `nautilus -q && nautilus`.

### PYTHONPATH workaround

If you use Homebrew Python on Ubuntu/Debian, Nautilus may fail to load the extension because the system `gi` module lives in `/usr/lib/python3/dist-packages/` which Homebrew Python doesn't include in its path. Add this to `~/.bashrc`:

```bash
export PYTHONPATH="/usr/lib/python3/dist-packages${PYTHONPATH:+:$PYTHONPATH}"
```

## Uninstall

```bash
rm ~/.local/share/nautilus-python/extensions/nautilus-diff-pdf.py
```

## Usage

Select exactly 2 PDF files in Nautilus, right-click, and choose **Diff PDFs**.
