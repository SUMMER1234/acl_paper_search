# ACL Literature Screening

## 1. Configure paths

Edit [file_paths.py](file_paths.py):

| Setting | Purpose |
| --- | --- |
| `ANTHOLOGY_DATABASE` | Full database to download and search |
| `FILTERED_BIB` | Matching papers saved as BibTeX |
| `CURRENT_RESULTS` | Current search results saved as Excel |
| `PREVIOUS_RESULTS` | Previous Excel results used for comparison |
| `UPDATED_ONLY_RESULTS` | New papers saved as Excel |

Use new filenames for each search. The archive path follows
`ANTHOLOGY_DATABASE` automatically; other filenames must be updated manually.
The `HISTORY` section lists old files for reference only.

## 2. Run in order

Run each file, or use these commands from this folder with
an interpreter containing `bibtexparser`, `pandas`, and `openpyxl`:

```bash
python download_anthology.py             # Download and extract
python search_rules.py                   # Search titles and abstracts
python bib_to_excel.py                   # Export matching papers to Excel
python updated_ref_from_last_search.py    # Export new papers only
```

- Skip downloading if the complete database already exists.

- Keep `KEYWORDS` unchanged to reuse the original search terms.



## 3. Record the run

Append the filenames, keywords, and console output to
`search_history.md` (local only, excluded from Git). This is a manual step.
