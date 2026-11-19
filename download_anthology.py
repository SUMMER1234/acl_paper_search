"""Download and extract ACL Anthology data using file_paths.py settings."""

import gzip
import shutil
from urllib.request import urlopen

if __package__:
    from . import file_paths as paths
else:
    import file_paths as paths


def download_database(url, archive_path, database_path):
    """Save the compressed download and extract its BibTeX contents."""
    if archive_path.exists() or database_path.exists():
        raise FileExistsError("Output already exists. Choose new paths in file_paths.py.")

    try:
        print("Downloading ACL Anthology...")
        with urlopen(url, timeout=60) as response, archive_path.open("wb") as output:
            shutil.copyfileobj(response, output)

        print("Extracting the database...")
        with gzip.open(archive_path, "rb") as source, database_path.open("wb") as output:
            shutil.copyfileobj(source, output)
    except Exception:
        # Remove incomplete files so the download can be retried.
        for file_path in (archive_path, database_path):
            if file_path.exists():
                file_path.unlink()
        raise

    print(f"Saved to: {database_path}")
    return database_path


if __name__ == "__main__":
    download_database(
        paths.ANTHOLOGY_DOWNLOAD_URL,
        paths.ANTHOLOGY_ARCHIVE,
        paths.ANTHOLOGY_DATABASE,
    )
