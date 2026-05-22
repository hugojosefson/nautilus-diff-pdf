import subprocess
import traceback
from typing import List
from urllib.parse import unquote

from gi.repository import Nautilus, GObject


class DiffPdfExtension(GObject.GObject, Nautilus.MenuProvider):
    """Nautilus extension for visually comparing two PDF files."""

    def uri_to_path(self, uri: str) -> str:
        """Convert a file URI to a local path."""
        return unquote(uri.replace("file://", ""))

    def diff_pdf_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        paths: tuple,
    ) -> None:
        """Handle the diff PDF menu activation."""
        path1, path2 = paths
        try:
            with subprocess.Popen(
                ["diff-pdf", "--view", path1, path2],
            ):
                pass
        except OSError as e:
            with open("/tmp/diff-pdf-error.log", "w", encoding="utf-8") as f:
                f.write(f"Error: {e}\n{traceback.format_exc()}\n")
                f.write(f"path1={path1}\npath2={path2}\n")

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        """Get menu items for selected files."""
        pdfs = [f for f in files if f.get_name().lower().endswith(".pdf")]
        if len(pdfs) != 2:
            return []

        paths = tuple(self.uri_to_path(f.get_uri()) for f in pdfs)

        item = Nautilus.MenuItem(
            name="NautilusDiffPdf::diff_pdfs",
            label="Diff PDFs",
            tip="Visually compare two PDF files",
        )
        item.connect("activate", self.diff_pdf_activate_cb, paths)

        return [item]

    def get_background_items(
        self,
        _current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        """Get background menu items (none for this extension)."""
        return []
