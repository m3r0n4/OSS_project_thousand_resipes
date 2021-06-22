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

def swap(x, i, j):
    x[i], x[j] = x[j], x[i]

def bubbleSort(x):
    for size in reversed(range(len(x))):
        for i in range(size):
            if x[i] > x[i+1]:
                swap(x, i, i+1)


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

def make_result(i1, i2, i3)
	name=es.get(index=foodname,doc_type='menu',id=1)
	link=es.get(index=foodname,doc_type='url',id=1)
	image=es.get(index=foodname,doc_type='img',id=1)
	ing=es.get(index=foodname,doc_type='food',id=1)

	result1 = [ name[i1], link[i1], image[i1], ing[i1] ]
	result2 = [ name[i2], link[i2], image[i2], ing[i2] ]
	result3 = [ name[i3], link[i3], image[i3], ing[i3] ]

	return result1, result2, result3

dic={ 'menu':[]
	'url':[]
	'food':[]
	'img':[]}
 #음식 이름과 해당 url 넣어주는 딕셔너리

#크롤링 한 후에 상위 10개 리스트 딕셔너리에 넣어주기!=>for문
#엘라스틱 서치 한개씩 불러와서 데이터 v1
#먹고 싶은 레시피 크롤링해서 불러와서 데이터 v2 
#for문으로 상위 10개 리스트=>10번 반복 (v1만 바꿔가면서 v1과 V2코사인 유사도 계산)
#max함수 사용하여 비교할 때마다 바꿔주기
#max값 v1리스트 반환하여 결과 페이지로 넘겨주기


es=Elasticsearch([{'host':es_host,'port':es_port}],timeout=100)

#es.index(index='foodname',doc_type='food',id=1,body=dic)
try :
	es.index(index='foodname',doc_type='url',id=1,body=dic)
	index=index_name
	want_list[]=#원하는 레시피 크롤링 내용 다 저장하기
	cleaning(want_list)
	process_new_sentence(want_list)
	v1=make_vector()
	s1=0
	s2=0
	s3=0
	idx1=0
	idx2=0
	idx3=0

	for i in range(0,10,1)
		res=es.get(index=foodname,doc_type='url',id=1)
		res[i]=#url통해 크롤링 페이지로 넘어가기
		craw_list[]#크롤링 레시피 내용 다 저장하기
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
		


	
if __name__ == '__main__':
	#메인에서 for문을 돌려서 elasticsearch의 레시피 v1
	#//			먹고 싶은 음식에 대한 레시피 받아와서 v2
	#result=cos_similarity(v1,v2) #for문 돌려야 할 듯,,
