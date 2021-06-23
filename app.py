#!/usr/bin/python3
#-*- coding: utf-8 -*-

from flask import Flask, jsonify 
from flask import render_template
from flask import request 
import argparse
import subprocess 
from elasticsearch import Elasticsearch
import soup
import cosine

es_host="127.0.0.1"
es_port="9200"

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	koreaID = soup.elasID()
	es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
	
	usares = es.get(index='usa', doc_type='chart', id=1) 
	usawordls = usares['_source']['words']

	canadares = es.get(index='canada', doc_type='chart', id=1)        
	canadawordls = canadares['_source']['words']

	koreares1 = es.get(index='korea', doc_type='chart', id=koreaID)        
	koreawordls1 = koreares1['_source']['words']
	korstr1 = "".join(koreawordls1)

	koreares2 = es.get(index='korea', doc_type='chart', id=koreaID-1)
	koreawordls2 = koreares2['_source']['words']
	korstr2 = "".join(koreawordls2)

	cosresult = round(cosine.cos(korstr1,korstr2)*100,2) 
	
	return render_template('index.html', kdata1=koreawordls1,kdata2=koreawordls2, data2=usawordls, data3=canadawordls,csr=cosresult) 



if __name__ == '__main__':
	app.run(debug=True)
