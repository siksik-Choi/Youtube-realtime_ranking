#!/usr/bin/python3
#-*- coding: utf-8 -*- 

from flask import Flask, jsonify
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/',methods = ['GET'])
def home():
        return render_template('startpage.html')

@app.route('/rank',methods=['GET'])
def ranking():
	error = None
	if request.method == 'GET':
		return render_template('rankingpage.html')

@app.route('/simil',methods=['GET'])
def similarlity():
	error = None
	if request.method == 'GET':
		return render_template('similarlity.html')


if __name__ == '__main__':
        app.run(debug=True)


