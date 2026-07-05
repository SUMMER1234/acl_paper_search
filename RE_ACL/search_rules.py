#coding=utf-8

import json
import re
import time
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

#read database
start_time = time.time()
with open("../anthology+abstracts (2) .bib", "r") as acl_file:
    bib_database = bibtexparser.load(acl_file)
    end_time = time.time()
    print("loading time: "+str(end_time-start_time))
print("There are "+str(len(bib_database.entries))+" papers")
print("Here is an example:")
print(bib_database.entries[1])
print("====="*10)


remove_chars = '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+'


title_list=[]
title_count = 0
for n,dict in enumerate(bib_database.entries):
    if "title" in dict.keys():
        clean_title = re.sub(remove_chars, "", dict["title"])
        title_list.append(clean_title+"_|||_"+str(n))
        title_count += 1
    # else:
    #     print(str(n)+" doesn't record title information")
print("Here are the number of data with titles: "+str(title_count))


abstract_list=[]
abstract_count = 0
for n,dict in enumerate(bib_database.entries):
    if "abstract" in dict.keys():
        clean_abstract = re.sub(remove_chars, "", dict["abstract"])
        abstract_list.append(clean_abstract+"_|||_"+str(n))
        abstract_count += 1
    # else:
    #     print(str(n)+" doesn't record abstract information")
print("Here are the number of data with abstract: "+str(abstract_count))


# keywords_list = ["qualitative study","qualitative analysis"]
keywords_list =  ["qualitative evaluation", "focus group", "interview", "observational study", "thematic analysis",
                 "grounded theory","qualitative study","qualitative analysis"]


#     [
#     "end user",
#     "Focus group research", "Focus group study", "Focus group analysis",
#     "interviews research", "interviews study", "interviews analysis",
#     "extrinsic evaluation",
#     "observation research", "observation study", "observation analysis",
#     "secondary research", "secondary study", "secondary analysis",
#     "error analysis",
#     "participatory design",
#     "nuance", "synthesis",
#     "impact evaluation",
#     "user studies",
#     "user-centered design",
#     "case studies",
#     "thematic analysis",
#     "grounded theory",
#     "qualitative coding",
#     "qualitative research", "qualitative study", "qualitative analysis",
#     "Ethnographic methods",
#     "ethnography",
#     "discourse research", "discourse study", "discourse analysis",
#     "participant observation",
#     "fieldwork",
#     "cultural probe",
#     "action research", "action study", "action analysis",
#     "phenomenological research", "phenomenological study", "phenomenological analysis"
# ]

keywords = "|".join(re.escape(k) for k in keywords_list)
print(keywords)


  # "[pP]atient(.*)[fF]eedback|[cC]linic [nN]ote|[Pp]atient(.*)[aA]ssess|[Pp]atient(.*)[Mm]onitor|" \
  #   "[Cc]ancer [sS]creen|[Cc]ancer [Ss]urviv|[Pp]atient(.*)[Ee]duca|[Cc]ancer [Cc]are|[Ss]elf.[mM]anage|" \
  #   "[Aa]ftercare|[Nn]eoplasm|[Ss]elf.care|[Cc]ancer [Dd]iagnos|[Cc]ancer [tT]reat|[Tt]umor|" \
  #   "[cC]hemotherapy|[Bb]ladder [Cc]ancer|[Bb]reast [cC]ancer|[Cc]olon and [rR]ectal [Cc]ancer|" \
  #   "[Ee]ndometrial|[Kk]idney|[Ll]eukemia|[Ll]iver [Cc]ancer|[Ll]ung [Cc]ancer|[Mm]elanoma|[Nn]on-[Hh]odgkin [Ll]ymphoma|" \
  #   "[Pp]ancreatic [cC]ancer|[Pp]rostate [cC]ancer|[Tt]hyroid [cC]ancer|[eE]lectronic [rR]ecord|" \
  #   "[Pp]atient(.*)[Aa]ctivit|[cC]linic information extract|[rR]adiotherapy [tT]reat|[dD]isease [tT]reat|" \
  #   "[Mm]edical(.*)[cC]hatbot|[mM]edical [cC]onversation|[mM]edical [rR]eport|[cC]linic(.*)[cC]hatbot|" \
  #   "[cC]linic(.*)[cC]onversation|[cC]linic(.*)[rR]eport|[Cc]ancer [pP]atient|[nN]ursing|[pP]atient(.*)[mM]ental|" \
  #   "[pP]atient(.*)[sS]entiment|[cC]linical decision.mak|[cC]ancer(.*)decision.mak"


title_search_result = list(filter(lambda x: re.search(keywords, x, re.IGNORECASE) != None, title_list))
abstract_search_result = list(filter(lambda x: re.search(keywords, x, re.IGNORECASE) != None, abstract_list))
print("Number of title matched data is "+ str(len(title_search_result)))
# print("Examples:")
# print(title_search_result[:10])
print("Number of abstract matched data is "+ str(len(abstract_search_result)))
# print("Examples:")
# print(abstract_search_result[:10])
print("====="*10)


total_filiter_bib_num=[]
total_search_results = []
for t in title_search_result:
    bib_num = t.split('_|||_')[1]
    total_search_results.append(bib_database.entries[int(bib_num)])
    total_filiter_bib_num.append(bib_num)

for a in abstract_search_result:
    bib_num = a.split('_|||_')[1]
    if bib_num not in total_filiter_bib_num:
        total_search_results.append(bib_database.entries[int(bib_num)])
        total_filiter_bib_num.append(bib_num)

print("There are "+str(len(total_search_results))+" matched")
print("Positions are "+str(total_filiter_bib_num))

# ["qualitative evaluation", "focus group", "interview", "observational study", "thematic analysis",
#                  "grounded theory", "ethnographic methods"]

#Export data
db = BibDatabase()
db.entries = total_search_results
writer = BibTexWriter()
writer.indent = '    '     # indent entries with 4 spaces instead of one
writer.comma_first = True  # place the comma at the beginning of the line
with open('ACL_qualitative_0926.bib', 'w') as bibfile:
    bibfile.write(writer.write(db))
print("Done!")

# with open('test_bibtex.bib', 'w') as bibtex_file:
#     bibtexparser.dump(db, bibtex_file)

