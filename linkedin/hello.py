from flask import Flask, jsonify, render_template, request
from linkedin import linkedin
import webbrowser	
import httplib2
app = Flask(__name__)
import Read_Data
import requests
from bs4 import BeautifulSoup
import dbms

API_KEY = 'f2wy1ympdfcr'
API_SECRET = 'wjXlB8Czxplt1mYK'
RETURN_URL = 'http://localhost:5000/redir.html'
		
@app.route('/_search')
def search():
	a = request.args.get('a', 0, type=str)
	res = Read_Data.work(a)
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
	app.run()
