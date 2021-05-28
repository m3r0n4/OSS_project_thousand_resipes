#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask

def hfilter(s):
	return re.sub(u'[^ \.\,\?\!u3130-\u318f\uac00-\ud7a3]+','',s)

situation = {'선택안함':'0','일상':'12', '초스피드':'18', '손님접대':'13', '간식':'17', '다이어트':'21', '야식':'45'}
if __name__ == '__main__':
	sit = input()
	lastcate = ""
	choice = "" 
	for key, value in situation.items():
		if key == sit:
			choice = value 
			if (value == '0'):
				lastcate = 'order'
			else:
				lastcate = 'cat2'
			break	
	url = 'https://www.10000recipe.com/recipe/list.html?q='
	url2 = '&query=&cat1=&cat2='+choice
	url_cat2 = '&cat3=&cat4=&fct=&order=accuracy&lastcate='+lastcate
	url_lastcate = '&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource='
	new_url = url+"소고기"+"+"+"계란"+url2+url_cat2+url_lastcate
	res = requests.get(new_url)
	html = BeautifulSoup(res.content, "html.parser")
	tags_title = html.select('div[class="common_sp_caption_tit line2"]')
	tags_link = html.select('a[class="common_sp_link"]')
#	for i in range(0,10):
	for i in range(0, len(tags_title)):
		html_content_title = hfilter(tags_title[i].text)
		print(html_content_title)		
#	for i in range(0,10):
#		html_content_link = tags_link[i]
#		print(html_content_link)
#print(new_url)
	count = 0
	for link in tags_link:
		if count == 10:
			break
		link_url = "https://www.10000recipe.com"+link["href"]
		print(link_url)
		count = count+1
