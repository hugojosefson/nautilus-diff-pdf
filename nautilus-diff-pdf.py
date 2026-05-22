import subprocess
from urllib.parse import unquote
from gi.repository import Nautilus, GObject
from typing import List


class DiffPdfExtension(GObject.GObject, Nautilus.MenuProvider):
    def uri_to_path(self, uri: str) -> str:
        return unquote(uri.replace("file://", ""))

    def diff_pdf_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        paths: tuple,
    ) -> None:
        path1, path2 = paths
        try:
            subprocess.Popen(
                ["diff-pdf", "--view", path1, path2],
            )
        except Exception as e:
            import traceback
            with open("/tmp/diff-pdf-error.log", "w") as f:
                f.write(f"Error: {e}\n{traceback.format_exc()}\n")
                f.write(f"path1={path1}\npath2={path2}\n")

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        pdfs = [f for f in files if f.get_name().lower().endswith(".pdf")]
        if len(pdfs) != 2:
            return []

        paths = tuple(self.uri_to_path(f.get_uri()) for f in pdfs)

        item = Nautilus.MenuItem(
            name="NautilusDiffPdf::diff_pdfs",
            label="Diff PDFs",
            tip="Compare two PDF files side by side",
        )
        item.connect("activate", self.diff_pdf_activate_cb, paths)

        return [item]

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        return []
