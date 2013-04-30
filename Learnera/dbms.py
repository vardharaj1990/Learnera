'''
Database Related functions
MongoDB operations

Collections: users, taken, courses, nonrelevant, coursemeta, user_relevance, isbn
'''
import pymongo

DB_SERVER='localhost'
DB_PORT=27017
DB_NAME='test'

class Database():
	def __init__(self):
		self.client = pymongo.MongoClient(DB_SERVER, DB_PORT)
		self.db = self.client[DB_NAME]

	'''
	Find user from the user collection with ID = uid
	'''		
	def find_user(self, ID):
		if self.db.users.find({"uid": ID}):
			return self.db.users.find({"uid": ID})[0]['info']
		else:
			return -1
		
	'''
	Insert user info into DB
	'''
	def insert_user(self, ret):
		if self.db.users.find({"uid" : ret['id']}).count() < 1: 
			self.db.users.insert({"uid": ret['id'], "info": ret})
	
	'''
	Update interests of a user
	'''
	def update_user_interests(self, ID, interest):
		ss = self.db.users.find({"uid":ID})[0]['info']['interests']
		ss += ', ' + interest
		self.db.users.update({"uid":ID}, {"$set": {"info.interests":ss}})
	
	'''
	Find user's connections
	'''	
	def find_connections(self, userid):
		if self.db.users.find({"uid":userid}).count() > 0:
			return self.db.users.find({"uid": userid})[0]['info']['connections']['values']
		
	'''
	Insert Course Info
	'''
	def insert_course(self, uid, course):
		self.db.courses.insert({"uid": uid, "info": course})
	
	'''
	Find courses based on ID
	'''
	def find_course(self, uid):
		if self.db.courses.find({"uid": ID}) != None:
			return self.db.courses.find({"uid": ID})[0]['info']
		else:
			return -1
		
	'''
	Insert courses to the "taken" collection
	'''
	def insert_taken(self, userid, courseid):
		self.db.taken.insert({"uid": userid, "course": courseid})
	
	'''
	Find taken courses by a user
	'''
	def find_taken(self, userid):
		taken = []
		cursor = self.db.taken.find({"uid": userid})
		for c in cursor:
			taken.append(c['course'])
		return list(set(taken))
	
	'''
	Inserting into the Not Relevant Collection
	'''
	def insert_nonrelevant(self, query, courseid):
		self.db.nonrelevant.insert({"query": query, "course": courseid})
	
	'''
	Find non relevant courses for a query
	'''
	def find_nonrelevant(self, query):
		non = []
		cursor = self.db.nonrelevant.find({"query": query})
		for c in cursor:
			non.append(c['course'])
		return non
	
	'''
	Insert into Course Meta Info Collection
	'''
	def insert_course_metainfo(self, courseid, user):
		self.db.coursemeta.insert({"courseid": courseid, "user": user})
	
	'''
	Find Course Meta Info
	'''
	def find_course_metainfo(self, courseid):
		users = []
		cursor = self.db.coursemeta.find({"courseid": courseid})
		
		for c in cursor:
			users.append(c['user'])
		return users
	
	'''
	Find attrib count for a course
	'''
	def find_course_attrib(self, courseid):
		attrib = {"basic": self.db.coursemeta.find({"courseid":courseid, "user.attrib":"basic"}).count(),
					"advanced": self.db.coursemeta.find({"courseid":courseid, "user.attrib":"advanced"}).count()}
		return attrib
	'''
	Insert into user_relevance Collection
	'''
	def insert_user_relevance(self, userid, courseid):
		self.db.user_relevance.insert({"uid":userid, "course": courseid})
	
	'''
	Find relevant courses for a user
	'''
	def find_user_relevance(self,userid):
		rel = []
		cursor = self.db.user_relevance.find({"uid": userid})
		for c in cursor:
			rel.append(c['course'])
		
		return list(set(rel))
	
	'''
	Insert <query, isbn> pair.
	'''
	def insert_isbn(self,query, isbn):
		if self.db.isbn.find({"query" : query}).count() < 1:
			self.db.isbn.insert({"query":query, "isbn":isbn})
	
	'''
	Find <query,isbn> pair from DB
	'''
	def find_isbn(self, query):
		isbn = []
		if self.db.isbn.find({"query" : query}).count() != 0:
			return self.db.isbn.find({"query" : query})[0]['isbn']
		else: 
			return None
	
	'''
	Insert <query, results> pair.
	'''
	def insert_queryresults(self, query, res):
		if self.db.queryresults.find({"query":query}).count() < 1: 
			self.db.queryresults.insert({"query":query, "results":res})
	
	'''
	Find results for a given query.
	'''
	def find_queryresults(self, query):
		if self.db.queryresults.find({"query" : query}).count() != 0:
			#print "query already issued"
			return self.db.queryresults.find({"query" : query})[0]['results']
		else:
			return None
	'''
	Update queryresults with filtered results.
	'''
	def update_queryresults(self, query, updated):
		self.db.queryresults.update({"query" : query},  {"$set": {"results":updated}})
		
	'''
	Insert < userid, courseid > pair.
	'''
	def insert_interested(self, userid, courseid):
		self.db.interested.insert({"uid":userid, "courseid":courseid})
		
	
	'''
	Get number of users who have liked this course.
	'''
	def find_interested_count(self, courseid):
		return self.db.interested.find({"courseid":courseid}).count()
		
	'''
	Get the users who have liked this course.
	'''
	def find_interested_users(self, courseid):
		cursor = self.db.interested.find({"courseid":courseid})
		users = []
		for cc in cursor:
			users.append(cc['uid'])
		
		return users
	
	'''
	Insert user specific interests. *Not Interested*
	'''
	def insert_notinterested(self, userid, courseid):
		self.db.notinterested.insert({"uid":userid, "courseid":courseid})
	
	'''
	Find user's *Not Interested* list.
	'''
	def find_notinterested(self, userid):
		cursor = self.db.notinterested.find({"uid":userid})
		courses = []
		for cc in cursor:
			courses.append(cc['courseid'])
		return courses
