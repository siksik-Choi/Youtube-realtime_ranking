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
	lastres = es.get(index='chart', doc_type='words', id=1)	

	eswordls = lastres['_source']['words']
	esfreqls = lastres['_source']['frequencies']		

	return render_template('index.html', data1=eswordls, data2=esfreqls) 



if __name__ == '__main__':
	app.run(debug=True)
