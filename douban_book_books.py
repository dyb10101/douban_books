# -*- coding: utf-8 -*-
import requests
import re
import os
from bs4 import BeautifulSoup
import shutil

page_url = 'https://book.douban.com/tag/%s?start=%d&type=T'

with open('hot_tags.txt', 'r') as f:
	for line in f:
		tag = line.strip()
		if not os.path.exists('./covers/' + tag):
			os.mkdir('./covers/' + tag)
		of = open('./books/' + tag + '.csv', 'w')

		for start in xrange(0, 2000, 20):
			url = page_url % (tag, start)

			r = requests.get(url)
			c = r.text
			if u'没有找到符合条件的图书' in c:
				break
			soup = BeautifulSoup(c, 'html.parser')
			for li in soup.findAll('li', class_='subject-item'):
				try:
					sid = li.h2.a['href'].split('/')[-2]
					main_title = li.h2.a['title'].strip()
					if li.h2.a.span is not None:
						sub_title = li.h2.a.span.get_text().strip()[1:].strip()
					else:
						sub_title = ''
					pub = li.find('div', class_='pub').get_text()
					arr = pub.split('/')
					if len(arr) == 5:
						author = arr[0].strip()
						trans = arr[1].strip()
						pu = arr[2].strip()
						date = arr[3].strip()
						price = arr[4].strip()
					elif len(arr) == 4:
						author = arr[0].strip()
						trans = ''
						pu = arr[1].strip()
						date = arr[2].strip()
						price = arr[3].strip()
					rating = li.find('span', class_='rating_nums').get_text().strip()
					ol = ','.join([sid, main_title, sub_title, author, trans, pu, date, price, rating])
					of.write(ol.encode('utf8') + '\n')

					cover_url = li.find('img')['src']
					ir = requests.get(cover_url, stream=True)
					with open('./covers/' + tag.decode('utf8') + '/' + sid + '_' + main_title + '.jpg', 'wb') as imf:
						ir.raw.decode_content = True
						shutil.copyfileobj(ir.raw, imf)

					print(ol)
				except:
					pass

		of.close()
