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


remove_chars = '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+'


#read general database
start_time = time.time()
with open("ACL_qualitative_0926.bib", "r") as screen_all:
    bib_database = bibtexparser.load(screen_all)
    end_time = time.time()
    print("loading time: "+str(end_time-start_time))
print("There are "+str(len(bib_database.entries))+" papers")


#Add keywords list
keywords =  ["qualitative evaluation", "focus group", "interview", "observational study", "thematic analysis",
                 "grounded theory","qualitative study","qualitative analysis"]

title_list=[]
abstract_list=[]
keywords_match_output=[]
Url_list=[]
for e in bib_database.entries:
    clean_title = re.sub(remove_chars, "", e["title"])
    title_list.append(clean_title)
    if "abstract" in e.keys():
        clean_abstract = re.sub(remove_chars, "", e["abstract"])
        abstract_list.append(clean_abstract)
        abstract_keywords_match=search_keywords(keywords,clean_abstract)
        if abstract_keywords_match:
            keywords_match_output.append(abstract_keywords_match)
        else:
            title_keywords_match = search_keywords(keywords, clean_title)
            keywords_match_output.append(title_keywords_match)
    else:
        abstract_list.append("")
        title_keywords_match = search_keywords(keywords, clean_title)
        keywords_match_output.append(title_keywords_match)
    if "url" in e.keys():
        Url_list.append(e["url"])
    else:
        Url_list.append("")

print("Here are the number of reference: "+str(len(bib_database.entries)))


data_chart={
    "title":title_list,
    "abstract":abstract_list,
    "keywords":keywords_match_output,
    "url":Url_list,

}
df = pd.DataFrame.from_dict(data=data_chart)
df.to_excel('Screen_result_1009.xlsx', index=False,encoding='utf-8-sig')
