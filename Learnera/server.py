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

def conn_data(db, user_id, temp):
	conn = db.find_connections(user_id)
	user_conn = []
	for cc in conn:
		user_conn.append(cc['id'])
	
	user_info = []	

	'''
	Gives number of ppl who have voted for this course from the current users connection
	'''
	def get_conn_count(uu):
		arr = 0
		for user in uu:
			if user_id != user and (user in user_conn):
				arr += 1
		return arr	
	
	for course in temp:
		arr = 0
		#Find Basic/Advanced Count, calculate num of connections who have liked
		usr = db.find_course_metainfo(course[1])
		attrib = db.find_course_attrib(course[1])
		int_users = list(set(db.find_interested_users(course[1])))
		print "interested_users: ", int_users
		user_info.append({"basic":attrib['basic'], "adv":attrib['advanced'], "likes":get_conn_count(int_users)})
	
	return user_info


@app.route('/_search')
def search():
	a = request.args.get('a', 0, type=str)
	user_id = request.args.get('uid', 0, type=str)
	query = a
	db = dbms.Database()
	res = db.find_queryresults(query)
	non_relevant = db.find_nonrelevant(query) 
	update = False
	#print "NR: "
	#print non_relevant
	if  res == None:
		res2 = Read_Data.work(query)
		temp = copy.deepcopy(res2)    	#Important - Deep copy of returned results list
	else:
		#print "Reading from DB..."
		if len(res) < 10:
			res = Read_Data.work(query)
			update = True
			print "Results < 10"
		temp = copy.deepcopy(res)
	
	non_relevant_flag = False
	
	temp2 = copy.deepcopy(temp)
		
	for course in temp2:
		if course[1] in non_relevant:
			print "Removing non-relevant course ", course[1]
			temp.remove(course)
			non_relevant_flag = True


	if non_relevant_flag or update:
		#print "Updating DB..."
		db.update_queryresults(query, temp)
	else:
		db.insert_queryresults(query, temp)
	
	if len(temp) > 10:
		temp = temp[0:10]	
	
	user_info = conn_data(db, user_id, temp)	
	print "User Info list: ", user_info
	#print "User not interested list: ", db.find_notinterested(user_id)
	ret = isbn.getisbnData(query)
	return jsonify(result = temp, result2 = ret, result3 = user_info)

@app.route('/_searchredir')
def searchredir():
	uid = request.args.get('uid', 0, type=str)
	username = request.args.get('username', 0, type=str)
	query = request.args.get('query',0, type=str)
	
	args = {'uid':uid, 'username': username, 'query': query}
	urlquery = urllib.urlencode(args)	
	url = 'http://localhost:5000/recommend.html?' + urlquery; 
	
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
	query = request.args.get('a', 0, type=str)
	course = request.args.get('b', 0, type=str)
	uid = request.args.get('c', 0 , type=str)
	db = dbms.Database()
	print "Inserting Non-relevant into DB ", query, course
	db.insert_nonrelevant(query, course)
	
	res = 'user '+ str(uid) + 'says ' + str(course) + ' is not relevant for ' + str(query)
	return jsonify(result = res)

@app.route('/_interested')
def interested():
	query = request.args.get('a', 0, type=str)
	course = request.args.get('b', 0, type=str)
	uid = request.args.get('c', 0 , type=str)
	db = dbms.Database()
	print "Inserting user interests into DB ", course, uid
	db.insert_interested(uid, course)
	
	res = 'Done'
	return jsonify(result = res)

@app.route('/_notinterested')
def notinterested():
	query = request.args.get('a', 0, type=str)
	course = request.args.get('b', 0, type=str)
	uid = request.args.get('c', 0 , type=str)
	db = dbms.Database()
	print "Inserting user interests into DB ", course, uid
	db.insert_notinterested(uid, course)
	
	res = 'Done'
	return jsonify(result = res)


@app.route('/_basic')
def basic():
	query = request.args.get('a', 0, type=str)
	course = request.args.get('b', 0, type=str)
	uid = request.args.get('c', 0 , type=str)
	res = 'user '+ uid + 'says ' + str(course) + ' is too basic for '
	User = {"id": uid, "attrib":"basic"}
	db = dbms.Database()
	
	db.insert_course_metainfo(course, User)
	return jsonify(result = res)

@app.route('/_advanced')
def advanced():
	query = request.args.get('a', 0, type=str)
	course = request.args.get('b', 0, type=str)
	uid = request.args.get('c', 0 , type=str)
	res = 'user '+ uid + 'says ' + str(c) + ' is too advanced for ' + str(d)
	User = {"id": uid, "attrib":"advanced"}
	db = dbms.Database()
	
	db.insert_course_metainfo(course, User)
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
