#!/usr/bin/python3
#-*- coding: utf-8 -*-

from flask import Flask, jsonify 
from flask import render_template
from flask import request 
import argparse
import subprocess 
from elasticsearch import Elasticsearch

es_host="127.0.0.1"
es_port="9200"

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
	usares = es.get(index='usa', doc_type='chart', id=1)	
	usawordls = usares['_source']['words']

	canadares = es.get(index='canada', doc_type='chart', id=1)        
	canadawordls = canadares['_source']['words']

	koreares = es.get(index='korea', doc_type='chart', id=1)        
	koreawordls = koreares['_source']['words']

	return render_template('index.html', data1=koreawordls, data2=usawordls, data3=canadawordls) 



if __name__ == '__main__':
	app.run(debug=True)
