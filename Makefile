PREFIX = $(HOME)/.local/share/nautilus-python/extensions
BASHRC = $(HOME)/.bashrc

.PHONY: install install-deps uninstall check

install: check
	@mkdir -p $(PREFIX)
	@cp extensions/diff-pdf.py $(PREFIX)/diff-pdf.py
	@if ! grep -qF 'nautilus-python needs system dist-packages' $(BASHRC); then \
		echo '' >> $(BASHRC); \
		echo '# nautilus-python needs system dist-packages for gi module' >> $(BASHRC); \
		echo 'export PYTHONPATH="/usr/lib/python3/dist-packages${PYTHONPATH:+:$PYTHONPATH}"' >> $(BASHRC); \
	fi
	@echo "Installed. Restart nautilus with: nautilus -q && nautilus"

uninstall:
	@rm -f $(PREFIX)/diff-pdf.py
	@sed -i '/nautilus-python needs system dist-packages/d' $(BASHRC)
	@sed -i '/^export PYTHONPATH="\/usr\/lib\/python3\/dist-packages/d' $(BASHRC)
	@echo "Uninstalled."

check:
	@command -v diff-pdf >/dev/null 2>&1 || { echo "Error: diff-pdf not found"; exit 1; }
	@dpkg -s gir1.2-nautilus-4.1 >/dev/null 2>&1 || { echo "Error: gir1.2-nautilus-4.1 not installed"; exit 1; }
	@dpkg -s python3-nautilus >/dev/null 2>&1 || { echo "Error: python3-nautilus not installed"; exit 1; }

install-deps:
	@sudo apt install -y gir1.2-nautilus-4.1 python3-nautilus
