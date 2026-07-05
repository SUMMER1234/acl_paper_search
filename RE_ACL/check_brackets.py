#coding = utf-8

import bibtexparser

with open('test_bibtex.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)
print(bib_database.entries[0])
