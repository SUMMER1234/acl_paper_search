#coding=utf-8

import json
import re
import time
import bibtexparser
import pandas as pd
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def search_keywords(keywords_list,text):
    pattern=re.compile('|'.join(keywords_list),re.IGNORECASE)
    search_result=pattern.findall(text)
    search_result=[s.lower() for s in search_result]
    result=",".join(set(search_result))
    return result

def index_match(match_list,new_db_path,match_pattern,target_list_for_update,update_pattern):
    with open(new_db_path, "r") as screen_subset:
        subset_bib_database = bibtexparser.load(screen_subset)

    for ref in subset_bib_database.entries:
        try:
            index = match_list.index(ref[match_pattern])
            target_list_for_update[index] = update_pattern
        except ValueError:
            print(str(ref[match_pattern])+"did not found in the database")
    print("There are "+str(len(subset_bib_database.entries))+" papers was indexed")
    return target_list_for_update




# def screen_result_match_database(No_bib_path,Yes_bib_path,Not_sure_bib_path,title_list):
#     with open(Yes_bib_path, "r") as screen_yes:
#         yes_bib_database = bibtexparser.load(screen_yes)
#
#     for ref in yes_bib_database.entries:
#         try:
#             index = title_list.index(ref["title"])
#             Screen_people_result[index] = "yes"
#         except ValueError:
#             print("YES paper not found in the database")
#
#     # NOT SURE
#     with open(Not_sure_bib_path, "r") as screen_notsure:
#         notsure_bib_database = bibtexparser.load(screen_notsure)
#
#     for ref in notsure_bib_database.entries:
#         try:
#             index = title_list.index(ref["title"])
#             Screen_people_result[index] = "not sure"
#         except ValueError:
#             print("NOT SURE paper not found in the database")


#read general database
start_time = time.time()
with open("screen_paper_all.bib", "r") as screen_all:
    bib_database = bibtexparser.load(screen_all)
    end_time = time.time()
    print("loading time: "+str(end_time-start_time))
print("There are "+str(len(bib_database.entries))+" papers")


#Add keywords list
keywords=["qualitative evaluation", "focus group", "interview", "observational study", "thematic analysis",
                 "grounded theory"]
title_list=[]
abstract_list=[]
keywords_match_output=[]
Url_list=[]
for e in bib_database.entries:
    title_list.append(e["title"])
    if "abstract" in e.keys():
        abstract_list.append(e["abstract"])
        abstract_keywords_match=search_keywords(keywords,e["abstract"])
        if abstract_keywords_match:
            keywords_match_output.append(abstract_keywords_match)
        else:
            title_keywords_match = search_keywords(keywords, e["title"])
            keywords_match_output.append(title_keywords_match)
    else:
        abstract_list.append("")
        title_keywords_match = search_keywords(keywords, e["title"])
        keywords_match_output.append(title_keywords_match)
    if "url" in e.keys():
        Url_list.append(e["url"])
    else:
        Url_list.append("")

print("Here are the number of reference: "+str(len(bib_database.entries)))



#read individual data_base
Summer_result=[0]*len(title_list)
No_bib_path="Summer/no.bib"
Yes_bib_path="Summer/yes.bib"
Not_sure_bib_path="Summer/notsure.bib"

Summer_result = index_match(title_list,No_bib_path,"title",Summer_result,"No")
Summer_result = index_match(title_list,Yes_bib_path,"title",Summer_result,"YES")
Summer_result = index_match(title_list,Not_sure_bib_path,"title",Summer_result,"NOT SURE")

#Dave
Dave_result=[0]*len(title_list)
Dave_No_bib_path="Dave/no.bib"
Dave_Yes_bib_path="Dave/yes.bib"
Dave_Not_sure_bib_path="Dave/notsure.bib"

Dave_result = index_match(title_list,Dave_No_bib_path,"title",Dave_result,"No")
Dave_result = index_match(title_list,Dave_Yes_bib_path,"title",Dave_result,"YES")
Dave_result = index_match(title_list,Dave_Not_sure_bib_path,"title",Dave_result,"NOT SURE")

#Adarsa
Adarsa_result=[0]*len(title_list)
Adarsa_No_bib_path="Adarsa/no.bib"
Adarsa_Yes_bib_path="Adarsa/yes.bib"
Adarsa_Not_sure_bib_path="Adarsa/notsure.bib"

Adarsa_result = index_match(title_list,Adarsa_No_bib_path,"title",Adarsa_result,"No")
Adarsa_result = index_match(title_list,Adarsa_Yes_bib_path,"title",Adarsa_result,"YES")
Adarsa_result = index_match(title_list,Adarsa_Not_sure_bib_path,"title",Adarsa_result,"NOT SURE")

data_chart={
    "title":title_list,
    "abstract":abstract_list,
    "keywords":keywords_match_output,
    "Summer":Summer_result,
    "Dave":Dave_result,
    "Adarsa":Adarsa_result,
    "url":Url_list,

}
df = pd.DataFrame.from_dict(data=data_chart)
df.to_csv('Screen_result_0730.csv', index=False,encoding='utf-8-sig')
