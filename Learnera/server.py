from flask import Flask, jsonify, render_template, request, redirect, Response
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
import urllib

@app.route('/_search')
def search():
	a = request.args.get('a', 0, type=str)
	user_id = request.args.get('uid', 0, type=str)
	query = a
	db = dbms.Database()
	res = db.find_queryresults(query)
	print user_id
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

		course.append(attrib['basic'])
		course.append(attrib['advanced'])
	ret = isbn.getisbnData(query)
	print user_info
	return jsonify(result = temp, result2 = ret)

@app.route('/_searchredir')
def searchredir():
	uid = request.args.get('uid', 0, type=str)
	username = request.args.get('username', 0, type=str)
	query = request.args.get('query',0, type=str)
	
	
	args = {'uid':uid, 'username': username, 'query': query}
	urlquery = urllib.urlencode(args)

	#url = 'http://localhost:5000/recommend.html?uid=' + uid + '&username=' + username + '&query=' + query;
	url =  'http://localhost:5000/recommend.html?' + urllib.urlencode(args)
	webbrowser.open(url)
	return

@app.route('/recommend.html')
def indexhtml():
	
	user_id = request.args.get('uid', 0, type=str)
	username = request.args.get('username', 0, type=str)
	query = request.args.get('query',0, type=str)
	
	return	render_template("recommend.html", uid = user_id, query=query, username = username)
	
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

	
@app.route('/_addinterest')
def addinterest():
	uid = request.args.get('uid', 0, type=str)
	a = request.args.get('b', 0, type=str)
	
	print "got a"
	print a
	print "got uid"
	print uid
	
	db = dbms.Database()
	db.update_user_interests(uid,a)
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
		db = dbms.Database()
		userdata = db.find_user(uid)
		#print db.find_user(uid)
		interests = userdata['interests'].split(',')
		
		
		for i in range(0,len(interests)):
			interests[i] = interests[i].strip().encode('ascii','ignore')
			#print interests[i]
			
		print userdata['skills']['values']
		for skill in userdata['skills']['values']:
			interests.append(skill['skill']['name'])
		
		entries = [dict(title=i, text=interests[i]) for i in range(0,len(interests))]	
		print interests
		print entries
		return render_template('home.html', uid = uid, username = lauth.user_name, interest=interests, entries=entries )		
	else:
		print "No Auth Code\n"
		return render_template('login.html')


if __name__ == '__main__':
	app.debug = True
	print 'calling preprocess'
	Read_Data.preprocess()
	app.run(debug=True, use_reloader=True)
	
	
