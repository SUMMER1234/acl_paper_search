"""Search ACL titles and abstracts for qualitative research keywords."""

import re
import time

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

if __package__:
    from . import file_paths as paths
else:
    import file_paths as paths


KEYWORDS = (
    "qualitative evaluation",
    "focus group",
    "interview",
    "observational study",
    "thematic analysis",
    "grounded theory",
    "qualitative study",
    "qualitative analysis",
)
KEYWORD_PATTERN = re.compile("|".join(re.escape(word) for word in KEYWORDS), re.IGNORECASE)
# Keep the original punctuation removal rules used by the screening workflow.
PUNCTUATION_PATTERN = re.compile('[·’!"\\#$%&\'()＃！（）*+,-./:;<=>?\\@，：?￥★、…．＞【】［］《》？“”‘’\\[\\]^_`{|}~]+')


def load_database(file_path):
    """Read a UTF-8 BibTeX database."""
    with open(file_path, encoding="utf-8") as bib_file:
        return bibtexparser.load(bib_file)


def find_matches(entries, field):
    """Return entry indices matching a keyword in the requested field."""
    matches = []
    for index, entry in enumerate(entries):
        if field not in entry:
            continue
        text = PUNCTUATION_PATTERN.sub("", entry[field])
        if KEYWORD_PATTERN.search(text):
            matches.append(index)
    return matches


def select_entries(entries, title_matches, abstract_matches):
    """Keep title matches first, then abstract-only matches in source order.

    Deduplicate by source index, preserving distinct database records even
    when they share a title or URL.
    """
    title_indices = set(title_matches)
    indices = title_matches + [
        index for index in abstract_matches if index not in title_indices
    ]
    return [entries[index] for index in indices]


def write_database(entries, file_path):
    """Export matching entries using the existing BibTeX formatting."""
    database = BibDatabase()
    database.entries = entries

    writer = BibTexWriter()
    writer.indent = "    "
    writer.comma_first = True
    with open(file_path, "w", encoding="utf-8") as bib_file:
        bib_file.write(writer.write(database))


def main():
    """Load, search, summarize, and export the configured ACL database."""
    start_time = time.perf_counter()
    database = load_database(paths.ANTHOLOGY_DATABASE)
    entries = database.entries
    print(f"Loading time: {time.perf_counter() - start_time:.2f} seconds")
    print(f"Total papers: {len(entries)}")
    print(f"Papers with titles: {sum('title' in entry for entry in entries)}")
    print(f"Papers with abstracts: {sum('abstract' in entry for entry in entries)}")
    print(f"Keywords: {', '.join(KEYWORDS)}")

    title_matches = find_matches(entries, "title")
    abstract_matches = find_matches(entries, "abstract")
    matched_entries = select_entries(entries, title_matches, abstract_matches)

    print(f"Title matches: {len(title_matches)}")
    print(f"Abstract matches: {len(abstract_matches)}")
    print(f"Unique matching papers: {len(matched_entries)}")

    write_database(matched_entries, paths.FILTERED_BIB)
    print(f"Results saved to: {paths.FILTERED_BIB}")


if __name__ == "__main__":
    main()
