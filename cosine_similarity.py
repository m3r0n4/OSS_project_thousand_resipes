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


dic={ 'crwal':{'foodname':[],'url':[]}} #음식 이름과 해당 url 넣어주는 딕셔너리

#크롤링 한 후에 상위 10개 리스트 딕셔너리에 넣어주기!=>for문
#엘라스틱 서치 한개씩 불러와서 데이터 v1
#먹고 싶은 레시피 크롤링해서 불러와서 데이터 v2 
#for문으로 상위 10개 리스트=>10번 반복 (v1만 바꿔가면서 v1과 V2코사인 유사도 계산)
#max함수 사용하여 비교할 때마다 바꿔주기
#max값 v1리스트 반환하여 결과 페이지로 넘겨주기


es=Elasticsearch([{'host':es_host,'port':es_port}],timeout=100)
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
sent_list=[]

#먹고 싶은 음식 레시피 크롤링한 것 받아오기(리스트 만들기) =>합칠 때
def process_new_sentence(s):
	sent_list.append(s)
	tokenized=okt.morphs(s)
	for word in tokenized:
		if word not in word_d.keys():
			word_d[word]=0
		word_d[word]+=1

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
	
if __name__ == '__main__':
	#메인에서 for문을 돌려서 elasticsearch의 레시피 v1
	#//			먹고 싶은 음식에 대한 레시피 받아와서 v2
	#result=cos_similarity(v1,v2) #for문 돌려야 할 듯,,
