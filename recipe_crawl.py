#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask

situation = {'선택안함':'0','일상':'12', '초스피드':'18', '손님접대':'13'}
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
	print(new_url)

