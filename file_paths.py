"""File paths for ACL screening scripts: active settings first, history last.

Paths are relative to this file, not the working directory. Dates in filenames
are manual labels; changing the database name does not rename search outputs.
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent


# === CURRENT: download_anthology.py -> search_rules.py ===

# download_anthology.py: remote download source.
ANTHOLOGY_DOWNLOAD_URL = "https://aclanthology.org/anthology+abstracts.bib.gz"

# download_anthology.py: extracted output; search_rules.py: input database.
ANTHOLOGY_DATABASE = PROJECT_DIR / "anthology_with_abstracts_20261119.bib"

# download_anthology.py: compressed output, named after ANTHOLOGY_DATABASE.
ANTHOLOGY_ARCHIVE = ANTHOLOGY_DATABASE.with_suffix(".bib.gz")


# === CURRENT: search_rules.py -> bib_to_excel.py ===

# search_rules.py: filtered output; bib_to_excel.py: input bibliography.
FILTERED_BIB = PROJECT_DIR / "ACL_qualitative_search_20261119.bib"

# bib_to_excel.py: output; updated_ref_from_last_search.py: current input.
CURRENT_RESULTS = PROJECT_DIR / "Screen_result_20261119.xlsx"


# === CURRENT: updated_ref_from_last_search.py ===

# Input baseline: an older result still actively used for comparison.
PREVIOUS_RESULTS = PROJECT_DIR / "Screen_result_20251009.xlsx"

# Output: papers whose URLs do not appear in PREVIOUS_RESULTS.
UPDATED_ONLY_RESULTS = PROJECT_DIR / "Screen_result_20261119_updated_only.xlsx"


# === HISTORY: reference only; not read or written by the current scripts ===

# Previously downloaded databases and archives in the project root.
# Preserve original filenames, including the space in the 20250718 filename.
ANTHOLOGY_DOWNLOADS = {
    "anthology+abstracts.bib": PROJECT_DIR / "anthology+abstracts.bib",
    "anthology+abstracts_0718.bib.gz": PROJECT_DIR / "anthology+abstracts_0718.bib.gz",
    "anthology+abstracts_20250718 .bib": PROJECT_DIR / "anthology+abstracts_20250718 .bib",
    "anthology_with_abstracts_20260705.bib": PROJECT_DIR / "anthology_with_abstracts_20260705.bib",
    "anthology_with_abstracts_20260705.bib.gz": PROJECT_DIR / "anthology_with_abstracts_20260705.bib.gz",
}

# Previous search outputs and intermediate files retained for reference.
REFERENCE_FILES = {
    'ACL_qualitative_0718.bib': PROJECT_DIR / 'ACL_qualitative_0718.bib',
    'ACL_qualitative_0926.bib': PROJECT_DIR / 'ACL_qualitative_0926.bib',
    'bibtex.bib': PROJECT_DIR / 'bibtex.bib',
    'searched_bibtex.bib': PROJECT_DIR / 'searched_bibtex.bib',
    'searched_bibtex_0.bib': PROJECT_DIR / 'searched_bibtex_0.bib',
    'searched_bibtex_0718_qualitative.bib': PROJECT_DIR / 'searched_bibtex_0718_qualitative.bib',
    'searched_bibtex_abstract_qualitative.bib': PROJECT_DIR / 'searched_bibtex_abstract_qualitative.bib',
    'searched_bibtex_qualitative.bib': PROJECT_DIR / 'searched_bibtex_qualitative.bib',
    'searched_bibtex_title_qualitative.bib': PROJECT_DIR / 'searched_bibtex_title_qualitative.bib',
}
REFERENCE_DIR = PROJECT_DIR / "searched_bibtex_0718_qualitative"
