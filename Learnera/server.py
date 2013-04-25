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

API_KEY = 'f2wy1ympdfcr'
API_SECRET = 'wjXlB8Czxplt1mYK'
RETURN_URL = 'http://localhost:5000/redir.html'

@app.route('/_search')
def search():
    a = request.args.get('a', 0, type=str)
    #b = request.args.get('b', 0, type=int)
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
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
	webbrowser.open(authentication.authorization_url)  # open this url on your browser
	return

@app.route('/')
def home():
	return render_template('login.html')

@app.route('/redir.html')
def redir():
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
	application = linkedin.LinkedInApplication(authentication)	

	if request.args.get('code', '') != '':
		authentication.authorization_code = request.args.get('code', '')
		authentication.get_access_token()
		ret = {}
		ret = application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations', 'interests', 'courses', 'following', 'related-profile-views', 'job-bookmarks', 'certifications'])
		db = dbms.Database()
		db.insert_user(ret)
		name = ret['firstName']
		return render_template('index.html')		
	else:
		print "No Auth Code\n"
		return render_template('login.html')

    
if __name__ == '__main__':
	app.debug = True
	Read_Data.preprocess()
	#mit_parse.preprocess()
	app.run()
