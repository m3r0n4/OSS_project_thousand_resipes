#!/usr/bin/python3
#-*-coding:utf-8-*-

from flask import *
from elasticsearch import Elasticsearch
from nltk import word_tokenize
from konlpy.tag import Okt
from konlpy.utils import pprint
from bs4 import BeautifulSoup

import sys
import re
import requests
import numpy

es_host="127.0.0.1"
es_port="9200"

def hfilter(s):
	return re.sub(u'[^ \.\,\?\!u3130-\u318f\uac00-\ud7a3]+', '', s)

def cleansing(text):  # 특수문자 제거 함수
	cleaned_text = re.sub('[-=+©,#/\?:;\{\}^$.@—{*\"※;»~&}%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text).replace("’", "").split()

	return cleaned_text



#cosine 계산 함
def cos_similarity(v1,v2):
	dotpro=numpy.dot(v1,v2)
	norm=(numpy.linalg.norm(v1)*numpy.linalg.norm(v2))
	similarity=dotpro/norm

	return similarity

okt=Okt()
word_d={}
word_d2={}
sent_list=[]
sent_list2=[]

def process_new_sentence(s):
	sent_list.append(s)
	tokenized=okt.morphs(s)
	for word in tokenized:
		if word not in word_d.keys():
			word_d[word]=0
		word_d[word]+=1

def process_new_sentence2(s):
	sent_list2.append(s)
	tokenized=okt.morphs(s)
	for word in tokenized:
		if word not in word_d2.keys():
			word_d2[word]=0
		word_d2[word]+=1

def make_vector(i):
	v=[]
	s=sent_list[i]	
	tokenized=okt.morphs(s)
	for w in word_d.keys():
		val=0
		for t in tokenized:
			if t==w:
				val+=1
		v.append(val)
	return v

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

	return pharse

def make_result(i1, i2, i3):
	name=es.get(index=foodname,doc_type='menu',id=1)
	link=es.get(index=foodname,doc_type='url',id=1)
	image=es.get(index=foodname,doc_type='img',id=1)
	ing=es.get(index=foodname,doc_type='food',id=1)

	result1 = [ name[i1], link[i1], image[i1], ing[i1] ]
	result2 = [ name[i2], link[i2], image[i2], ing[i2] ]
	result3 = [ name[i3], link[i3], image[i3], ing[i3] ]

	return result1, result2, result3

def make_es(menu, url, food, img, want):
	dic={ 'menu':menu, 
		'url':url, 
		'food':food, 
		'img':img}
	es=Elasticsearch([{'host':es_host,'port':es_port}],timeout=100)
	#es.index(index='foodname',doc_type='food',id=1,body=dic)
	es.index(index='foodname',doc_type='url',id=1,body=dic)
	index=index_name
	want_list=recipe_crawl(want)
	cleaning(want_list)
	process_new_sentence(want_list)
	v1=make_vector()
	s1=0
	s2=0
	s3=0
	idx1=0
	idx2=0
	idx3=0
	res=es.get(index=foodname,doc_type='url',id=1)

	for i in range(0,len(res),1):
		craw_list=recipe_crawl(res[i])
		cleaning(craw_list)
		process_new_sentence2(craw_list)
		v2=make_vector()

		now=cos_similarity(v1,v2)

		if (now > s1):
			idx3=idx2
			s3=s2
			idx2=idx1
			s2=s1
			idx1=i
			s1=now
		elif (now > s2):
			idx3=idx2
			s3=s2
			idx2=i
			s2=now
		elif (now > s3):
			idx3=i
			s3=now
	
	return make_result(idx1, idx2, idx3)

def crawling(gri1, gri2, gri3, cate, want):
	situation = {'선택안함': '0', '일상': '12', '초스피드': '18', '손님접대': '13'}
	sit = cate
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
	new_url = url+gri1+"+"+gri2+"+"+gri3+url2+url_cat2+url_lastcate
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

	want_url = "https://www.10000recipe.com/recipe/6830006"

	return make_es(picked_name, picked_link, ingredient, picked_image, want_url)


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route('/step1', methods=["GET", "POST"])
def step1():
    error = None
    return render_template('step1.html')

@app.route('/step2', methods=["GET", "POST"])
def step2():
    error = None
    if request.method == 'POST':
        gri1 = request.form['gri1']
        gri2 = request.form['gri2']
        gri3 = request.form['gri3']
        return render_template('step2.html', gri1 = gri1, gri2 = gri2, gri3 = gri3)
    else:
        gri1 = request.args.get['gri1']
        gri2 = request.args.get['gri2']
        gri3 = request.args.get['gri3']
        return render_template('step2.html', gri1 = gri1, gri2 = gri2, gri3 = gri3)

@app.route('/step3', methods=["GET", "POST"])
def step3():
    error = None
    if request.method == 'POST':
        gri1 = request.form['gri1']
        gri2 = request.form['gri2']
        gri3 = request.form['gri3']
        cate = request.form['cate']
        return render_template('step3.html', gri1 = gri1, gri2 = gri2, gri3 = gri3, cate = cate)
    else:
        gri1 = request.args.get['gri1']
        gri2 = request.args.get['gri2']
        gri3 = request.args.get['gri3']
        cate = request.args.get['cate']
        return render_template('step3.html', gri1 = gri1, gri2 = gri2, gri3 = gri3, cate = cate)

@app.route('/result', methods=["GET", "POST"])
def result():
    error = None
    if request.method == 'POST':
        gri1 = request.form['gri1']
        gri2 = request.form['gri2']
        gri3 = request.form['gri3']
        cate = request.form['cate']
        want = request.form['want']
        result1 = []
        result2 = []
        result3 = []
        result1, result2, result3 = crawling(gri1, gri2, gri3, cate, want)
        return render_template('result.html', name1 = result1[0], name2 = result2[0], name3 = result3[0], link1 = result1[1], link2 = result2[1], link3 = result3[1], img1 = result1[2], img2 = result2[2], img3 = result3[2], gri1 = result1[3], gri2 = result2[3], gri3 = result3[3])
    else:
        gri1 = request.args.get['gri1']
        gri2 = request.args.get['gri2']
        gri3 = request.args.get['gri3']
        cate = request.args.get['cate']
        want = request.args.get['want']
        result1 = []
        result2 = []
        result3 = []
        result1, result2, result3 = crawling(gri1, gri2, gri3, cate, want)
        return render_template('result.html', name1 = result1[0], name2 = result2[0], name3 = result3[0], link1 = result1[1], link2 = result2[1], link3 = result3[1], img1 = result1[2], img2 = result2[2], img3 = result3[2], gri1 = result1[3], gri2 = result2[3], gri3 = result3[3])
    
if __name__ == '__main__':
    app.run()
