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
	db = dbms.Database()
	res = db.find_queryresults(query)
	
	if  res == None:
		print "res None"
		res = Read_Data.work(query)
	
	for course in res:
		if course[0] == 'coursera':
			attrib = db.find_course_attrib(course[1])
		else:
			attrib = db.find_course_attrib(course[8])
		course.insert(3,attrib['basic'])
		course.insert(4,attrib['advanced'])
	

	ret = isbn.getisbnData(query)
	
	db.insert_queryresults(query, res)
	return jsonify(result = res, result2 = ret)

@app.route('/_relevant')
def relevant():
	a = request.args.get('a', 0, type=str)
	b = request.args.get('b', 0, type=str)
	uid = request.args.get('uid', 0 , type=str)
	res = 'user '+ uid + 'says ' + str(a) + ' is not relevant for ' + str(b)
	return jsonify(result = res)

@app.route('/_basic')
def basic():
	c = request.args.get('c', 0, type=str)
	d = request.args.get('d', 0, type=str)
	uid = request.args.get('uid', 0 , type=str)
	res = 'user '+ uid + 'says ' + str(c) + ' is too basic for ' + str(d)
	User = {"id": uid, "attrib":"basic"}
	db = dbms.Database()
	
	db.insert_course_metainfo(c, User)
	return jsonify(result = res)

@app.route('/_advanced')
def advanced():
	c = request.args.get('c', 0, type=str)
	d = request.args.get('d', 0, type=str)
	uid = request.args.get('uid', 0 , type=str)
	res = 'user '+ uid + 'says ' + str(c) + ' is too advanced for ' + str(d)
	User = {"id": uid, "attrib":"advanced"}
	db = dbms.Database()
	
	db.insert_course_metainfo(c, User)
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
		uid = lauth.user_id
		print uid
		return render_template('index.html', uid = uid, username = lauth.user_name)		
	else:
		print "No Auth Code\n"
		return render_template('login.html')

    
if __name__ == '__main__':
	app.debug = True
	Read_Data.preprocess()
	app.run()
