#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from konlpy.utils import pprint
import sys
from elasticsearch import Elasticsearch

es_host="127.0.0.1"
es_port="9200"

word_count = {}

def clean(inlist):
	outlist = []
	for word in inlist:
		symbols = """!?,.()"""
		for i in range(len((symbols))):
			word = word.replace(symbols[i],'')
		if len(word) > 0: 
			outlist.append(word)
	return outlist

def filter(s):
	return re.sub('[\n \t \. \, \? \!]','',s)

def count(s):
	for word in s:
		if word in word_count.keys():
			word_count[word] += 1
		word_count[word] = 1

if __name__ == '__main__':
	url = u'https://en.wikipedia.org/wiki/Web_crawler'
	res = requests.get(url)
	
	html = BeautifulSoup (res.content, "html.parser")

	html_body = html.find(attrs={"class":"mw-parser-output"}) 
	body = html_body.find_all('p') 
	for item in body:
		body2 = item.getText()
		wl = body2.lower().split()	
		wf = clean(wl)
		for word in wf:
			if word in word_count.keys():
				word_count[word] += 1	
			else:
				word_count[word] = 1
		word_countt = sorted(word_count.items(), reverse=True, key=lambda x:x[1])
	print(type(word_countt))		
#	print(word_countt)
	
	words = list()
	freq = list()		
	for i in range(0,10):
		words.append(word_countt[i][0])
		freq.append(word_countt[i][1])




#	words = list(word_countt.keys())
#	freq = list(word_countt.values())		
	print("words len:",len(words))
	print("freq len:",len(freq))

	es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)

	e1 = {"url":url, "words":words, "frequencies":freq} 
	
	elasres = es.index(index='web', doc_type='words', id=1, body=e1)
#	print(elasres)
	
	lastres = es.get(index='web', doc_type='words', id=1)
	print(type(lastres.keys()))
#	print(lastres)
	
