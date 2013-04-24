'''
Database Related functions
MongoDB operations
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
		if self.db.users.find({"uid": ID}) != None:
			return self.db.users.find({"uid": ID})[0]
		else:
			return -1
		
	'''
	Insert user info into DB
	'''
	def insert_user(self, ret):
		self.db.users.insert({"uid": ret['id'], "info": ret})
		
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
			return self.db.courses.find({"uid": ID})[0]
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
	Insert into user_relevance Collection
	'''
	def insert_user_relevance(self, userid, courseid):
		self.db.user_relevance({"uid":userid, "course": courseid})
	
	'''
	Find relevant courses for a user
	'''
	def find_user_relevance(self,userid):
		rel = []
		cursor = self.db.user_relevance.find({"uid": userid})
		for c in cursor:
			rel.append(c['course'])
		
		return list(set(rel))


