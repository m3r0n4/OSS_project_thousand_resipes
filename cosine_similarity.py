#!/usr/bin/python3
#-*- coding: utf-8 -*-

from elasticsearch import Elasticksearch
from nltk import word_tokenize
from konlpy.tag import Okt
from konlpy.utils import pprint

import sys
import re
import numpy

es_host="127.0.0.1"
es_port="9200"


app=Flask(__name__)

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
word_d2{}
sent_list=[]
sent_list2=[]


#먹고 싶은 음식 레시피 크롤링한 것 받아오기(리스트 만들기) =>합칠 때
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

#엘라스틱 서치의 레시피 주요 단어 리스트 받아오기
#벡터 만들기 함수
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

dic={ 'menu':[]
	'url':[]
	'food':[]
	'img':[]}

es=Elasticsearch([{'host':es_host,'port':es_port}],timeout=100)

#es.index(index='foodname',doc_type='food',id=1,body=dic)
try :
	es.index(index='foodname',doc_type='url',id=1,body=dic)
	index=index_name
	want_list[]=#원하는 레시피 크롤링 내용 다 저장하기
	cleaning(want_list)
	process_new_sentence(want_list)
	v1=make_vector()

	for i in range(0,10,1)
		res=es.get(index=foodname,doc_type='url',id=1)
		res[i]=#url통해 크롤링 페이지로 넘어가기
		craw_list[]#크롤링 레시피 내용 다 저장하기
		cleaning(craw_list)
		process_new_sentence2(craw_list)
		v2=make_vector()

		result[i]=cos_similarity(v1,v2)
	bubbleSort(result)

		

		
		
		
		
	
	
index=index_name
res=es.get(index=foodname,doc_type='food',id=1)



	
if __name__ == '__main__':
	#메인에서 for문을 돌려서 elasticsearch의 레시피 v1
	#//			먹고 싶은 음식에 대한 레시피 받아와서 v2
	#result=cos_similarity(v1,v2) #for문 돌려야 할 듯,,
