"""Offline checks for downloading and extracting the Anthology database."""

import gzip
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "RE_ACL"))
import download_anthology


class DownloadTests(unittest.TestCase):
    def test_download_and_extract(self):
        content = b'@article{example, title={Example}}\n'
        compressed = gzip.compress(content)
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "data.bib.gz"
            database = Path(directory) / "data.bib"
            with patch.object(download_anthology, "urlopen", return_value=io.BytesIO(compressed)):
                download_anthology.download_database("https://example.org/data.gz", archive, database)
            self.assertEqual(archive.read_bytes(), compressed)
            self.assertEqual(database.read_bytes(), content)

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "data.bib.gz"
            database = Path(directory) / "data.bib"
            database.write_bytes(b"existing data")
            with patch.object(download_anthology, "urlopen") as request:
                with self.assertRaises(FileExistsError):
                    download_anthology.download_database("https://example.org/data.gz", archive, database)
                request.assert_not_called()
            self.assertEqual(database.read_bytes(), b"existing data")

    def test_broken_download_leaves_no_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "data.bib.gz"
            database = Path(directory) / "data.bib"
            with patch.object(download_anthology, "urlopen", return_value=io.BytesIO(b"not gzip")):
                with self.assertRaises(OSError):
                    download_anthology.download_database("https://example.org/data.gz", archive, database)
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
