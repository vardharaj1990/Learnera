from linkedin import linkedin

API_KEY = 'f2wy1ympdfcr'
API_SECRET = 'wjXlB8Czxplt1mYK'
RETURN_URL = 'http://psi.cse.tamu.edu/people/virendra-karappa'

authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
print authentication.authorization_url  # open this url on your browser
application = linkedin.LinkedInApplication(authentication)

authentication.authorization_code = raw_input("Enter code")
authentication.get_access_token()
#application.get_profile()
print application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations', 'summary', 'interests', 'recommendations-received', 'following'])


#print application.get_connections()
