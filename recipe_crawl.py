#!/usr/bin/python3
#-*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask
def hfilter(s):
	return re.sub(u'[^ \.\,\?\!u3130-\u318f\uac00-\ud7a3]+', '', s)

def recipe_crawl(crawl_url):
	pharse = []
	get_url = requests.get(crawl_url)	
	html_recipe = BeautifulSoup(get_url.content, "html.parser")
	tags_recipe = html_recipe.select("#stepdescr1")
	pharse.append(tags_recipe[0].text)
	tags_recipe = html_recipe.select("#stepdescr2")
	pharse.append(tags_recipe[0].text)
	tags_recipe = html_recipe.select("#stepdescr3")
	pharse.append(tags_recipe[0].text)
	try:
		divdata = html_recipe.select("#stepdescr4")
	except AttributeError as err:
		print("no tags\n")
	else:
		pharse.append(tags_recipe[0].text)
	try:
		divdata = html_recipe.select("#stepdescr5")
	except AttributeError as err:
		print("no tags\n")
	else:
		pharse.append(tags_recipe[0].text)

	print(pharse)
	return pharse
situation = {'선택안함': '0', '일상': '12', '초스피드': '18', '손님접대': '13', '간식': '17', '다이어트': '21', '야식': '45'}
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
	name = []
	count_title = 0
	for i in range(0, len(tags_title)):
		if count_title == 10:
			break
		html_content_title = hfilter(tags_title[i].text)
   #   print(html_content_title)
		name.append(html_content_title)
		count_title = count_title+1  
	print('\n')
	link_list = []
	count = 0
	for link in tags_link:
		if count == 10:
			break
		link_url = "https://www.10000recipe.com"+link["href"]
		link_list.append(link_url)
   #   print(link_url)
		count = count+1
	print(name)
	print(link_list)
	name_dict = {}
	link_dict = {}
	name_dict['name'] = name
	link_dict['link'] = link_list
	print(name_dict)
	print(link_dict)
	image_dict = {}
	image = []
	ingredients_dict = {}
	ingredient = []
	picked_name = []
	picked_link = []
	picked_image = []
	img_count = 0
	ing_count = 0
	ingre_list = []
	for l in link_list:
		if img_count == 10:
			break
		r = requests.get(l)
		html_link = BeautifulSoup(r.content, "html.parser")
#      tags_img = html_link.select("#main_thumbs")   
		tags_img = html_link.find('img', id = 'main_thumbs')
#      tags_img = html_link.find_all('img')
		img = tags_img['src']
		image.append(img)
		image_dict['image'] = image
	#	temp_list = []
		try:
			divdata = html_link.find('div',{"class":"ready_ingre3"})	
			redata = divdata.select('ul > a > li')
		except AttributeError as err:
			print("no tags\n")
		else:
			temp_list = []
			for pdata in redata:
				unsplited_ing = pdata.get_text()
				splited_ing = unsplited_ing.split("\n")
				unzero = splited_ing[0].replace(" ", "")
				temp_list.append(unzero)
			ingredient.append(temp_list)
			picked_name.append(name[img_count])
			picked_link.append(l)
			picked_image.append(image[img_count])
		img_count = img_count + 1
		print(temp_list)
	#	ingredient.append(temp_list)
	print(ingredient)
	print(image_dict)
	print(picked_name)
	print(picked_link)
	print(picked_image)
	pharse = []
	pharse = recipe_crawl('https://www.10000recipe.com/recipe/6947579')
	
