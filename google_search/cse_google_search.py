#coding=utf-8
#!/usr/bin/env python3

import requests

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "AIzaSyC0wmQvh9zi79zKYsYiVCugOMwHb1JmHww"
# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = "e37d8b6a21d154516"



# the search query you want
query = "'patient? feedback' OR 'clinic note?'"
query = query.replace("\"","'")

page = 1
start = (page - 1) * 10 + 1

url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
print(url)
# url='https://aclanthology.org/2021.winlp-1.4/#'
data = requests.get(url).json()
# print(data.content)
search_items = data.get("items")
print(search_items)
if search_items:
    page=+1

