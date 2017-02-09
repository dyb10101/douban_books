# -*- coding: utf-8 -*-
import requests
import re

hot_tag_index_page_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'

r = requests.get(hot_tag_index_page_url)
c = r.text

mat = re.findall(ur'<td><a href="/tag/(.+)">', c)

with open('./hot_tags.txt', 'w') as f: 
	for tag in mat:
		f.write(tag.encode('utf8') + '\n')

print('Done')