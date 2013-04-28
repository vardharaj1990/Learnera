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
import copy

@app.route('/_search')
def search():
	a = request.args.get('a', 0, type=str)
	user_id = request.args.get('uid', 0, type=str)
	query = a
	db = dbms.Database()
	res = db.find_queryresults(query)
	
	#Important - Deep copy of returned results list
	if  res == None:
		res2 = Read_Data.work(query)
		temp = copy.deepcopy(res2)
	else:
		temp = copy.deepcopy(res)
	
	db.insert_queryresults(query, temp)
	user_info = []
	
	user_conn = []
	conn = db.find_connections(user_id)
	for cc in conn:
		user_conn.append(cc['id'])
		
	'''
	Gives number of ppl who have voted for this course from the current users connection
	'''
	def get_conn_count(uu):
		arr = 0
		for user in uu:
			if user_id != user['id'] and (user['id'] in user_conn):
				#print "Conn has rated the same course:", user['id']
				arr += 1
		return arr
	
	for course in temp:
		arr = 0
		#Find Basic/Advanced Count, calculate num of connections who have voted
		#Coursera
		if course[0] == 'coursera':
			attrib = db.find_course_attrib(course[1])
			usr = db.find_course_metainfo(course[1])
			
			user_info.append(get_conn_count(usr))		
		
		#MIT
		elif course[0] == 'mit':
			attrib = db.find_course_attrib(course[8])
			usr = db.find_course_metainfo(course[8])
			user_info.append(get_conn_count(usr))		
		#YouTube
		else:
			usr = db.find_course_metainfo(course[4])
			user_info.append(get_conn_count(usr))
			attrib = db.find_course_attrib(course[4])

		course.insert(3,attrib['basic'])
		course.insert(4,attrib['advanced'])
	ret = isbn.getisbnData(query)
	print user_info
	return jsonify(result = temp, result2 = ret)

@app.route('/_relevant')
def relevant():
	a = request.args.get('a', 0, type=str)
	b = request.args.get('b', 0, type=str)
	uid = request.args.get('uid', 0 , type=str)
	res = 'user '+ uid + 'says ' + str(a) + ' is not relevant for ' + str(b)
	db = dbms.Database()
	db.insert_nonrelevant(b, a)
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
