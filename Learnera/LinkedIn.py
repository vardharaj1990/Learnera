from linkedin import linkedin
import dbms

API_KEY = 'f2wy1ympdfcr'
API_SECRET = 'wjXlB8Czxplt1mYK'
RETURN_URL = 'http://localhost:5000/redir.html'

class Auth():
	def __init__(self):
		self.authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
		self.application = linkedin.LinkedInApplication(self.authentication)
		self.user_id = ""
	
	def auth_url(self):
		return self.authentication.authorization_url

	def app():
		return application

	def get_data(self, code):
		self.authentication.authorization_code = code
		self.authentication.get_access_token()
		ret = {}
		ret = self.application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations', 'interests', 'courses', 'following', 'related-profile-views', 'job-bookmarks', 'certifications', 'connections'])
		self.user_id = ret['id']
		self.user_name = ret['firstName']
		write_to_db(ret)


def write_to_db(ret):
	db = dbms.Database()
	db.insert_user(ret)
		


