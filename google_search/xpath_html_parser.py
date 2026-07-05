#coding=utf-8
#!/usr/bin/env python3


from lxml import etree
import requests
from lxml.html import fromstring, tostring
url = "https://aclanthology.org/2021.winlp-1.4/"

ret = requests.get(url)
code = ret.apparent_encoding  # 获取url对应的编码格式
ret.encoding = code
html = ret.text               # html文件内容即示例中的标签
print(html)

# tree = etree.HTML(html)
# result = tree.xpath('//*[@id="lh"]')
# print(result)
# print('看结果这里', tostring(result, encoding=code).decode(code))

