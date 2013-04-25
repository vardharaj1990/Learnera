from flask import Flask, jsonify, render_template, request, redirect
app = Flask(__name__)
import Read_Data
import mit_parse
import spell_check
import isbn
from linkedin import linkedin
import webbrowser
import dbms
import requests
import LinkedIn

@app.route('/_search')
def search():
    a = request.args.get('a', 0, type=str)
    b = [spell_check.correct(x) for x in a.split()]
    actual_q = ''
    for word in a.split():
    	actual_q = actual_q + word + ' '
    	
    query = ''
    for word in b:
    	query = query + word + ' '

    res = Read_Data.work(query)
    return jsonify(result = res)

@app.route('/_relevant')
def relevant():
	a = request.args.get('a', 0, type=str)
	b = request.args.get('b', 0, type=str)
	res = a + ' is not relevant for ' + b
	return jsonify(result = res)

    
@app.route('/_search_isbn')
def search_mit():
	a = request.args.get('a', 0, type=str)
	b = [spell_check.correct(x) for x in a.split()]
	actual_q = ''
	for word in a.split():
		actual_q = actual_q + word + ' '
	
	query = ''
	for word in b:
		query = query + word + ' '
	res = isbn.getisbnData(query)
	return jsonify(result = res)
	
@app.route('/_login')
def login():
	lauth = LinkedIn.Auth()
	url = lauth.auth_url()
	webbrowser.open(url)  # open this url on your browser
	return

@app.route('/')
def home():
	return render_template('login.html')

@app.route('/redir.html')
def redir():
	lauth = LinkedIn.Auth()	
	if request.args.get('code', '') != '':
		code = request.args.get('code', '')
		lauth.get_data(code)
		return render_template('index.html')		
	else:
		print "No Auth Code\n"
		return render_template('login.html')

    
if __name__ == '__main__':
	app.debug = True
	Read_Data.preprocess()
	#mit_parse.preprocess()
	app.run()
