import sys
import os
import re
from collections import defaultdict
import json
import math
import requests
import pprint
import random
import urllib

def func():
    return defaultdict(float)

def func2():
    return defaultdict(func())

links = set()
social_links = set()
num_courses = 0
course_id = set()
course_tf = defaultdict(func)
course_idf = defaultdict(float)
clusters = defaultdict(set)
course_text = defaultdict(str)
course_cat = defaultdict(set)
course_tfidf = defaultdict(func)
query = defaultdict(float)
q_result = defaultdict(float)
centroid = defaultdict(func)
course_details = defaultdict(list)


def read_json():
    f = open("fullcourses.txt", 'w')
    r = requests.get("https://www.coursera.org/maestro/api/topic/list?full=1")
    json.dump(r.json(), f)
    f.close()

def read_course_json():
    f = open("courses.txt", 'w')
    for name in short_names:
        r = requests.get("https://www.coursera.org/maestro/api/topic/information?topic-id=" + name)
        json.dump(r.json(),f)
        f.write('\n')
    f.close()

def tf_add(tok,d_id):
    global course_tf
    for word in tok:
        course_tf[d_id][word] += 1
    for word in tok:
        val = course_tf[d_id][word]
        course_tf[d_id][word] = 1 + math.log(val,2)

def idf_add(tok):
    global course_idf
    tok_s = set(tok)
    for word in tok_s:
        course_idf[word] += 1

def calc_idf():
    global course_idf
    global num_courses
    for key in course_idf:
        course_idf[key] = math.log((float(num_courses)/course_idf[key]),2)

def calc_tfidf():
    global course_idf
    global course_tf
    global course_tfidf

    for doc_id in course_tf:
        norm = 0
        for term in course_tf[doc_id]:
            course_tfidf[doc_id][term] = course_tf[doc_id][term] * course_idf[term]
            norm += course_tfidf[doc_id][term] * course_tfidf[doc_id][term]
        norm = math.sqrt(norm)
        for term in course_tfidf[doc_id]:
                course_tfidf[doc_id][term] = course_tfidf[doc_id][term] / norm

def process_json():
	global num_courses 
	f = open("mit_ocw.txt", 'rU')
	content = f.readlines()
	for line in content:
		r = json.loads(line)
		for courses in r['Results']:
			
			if 'Description' not in courses:
				continue
			num_courses += 1
			
			course_id.add(courses['UniqueID'])
			details = []
			
			
			if 'CourseURL' in courses:
				details.append(courses['CourseURL'])
			else:
				details.append('')
				
			if 'Title' in courses:
				details.append(courses['Title'])
			else:
				details.append('')
			
			
			if 'Description' in courses:
				details.append(courses['Description'])
			else:
				details.append('')
			
			if 'InstitutionNameFull' in courses:
				details.append(courses['InstitutionNameFull'])
			else:
				details.append('')
			
			if 'Instructors' in courses:
				details.append(courses['Instructors'])	
			else:
				details.append('')
			
				
			if 'TeachingDate' in courses:
				details.append(courses['TeachingDate'])
			else:
				details.append('')
			
			if 'DownloadPageLink' in courses:
				details.append(courses['DownloadPageLink'])
			else:
				details.append('')
			'''

			if 'CourseLanguage' in courses:
				details.append(courses['CourseLanguage'])
			else:
				details.append('')
			
			
			if 'CourseSection' in courses:
				details.append(courses['CourseSection'])
			else:
				details.append('')
			'''
			
			clusters[courses['CourseSection']].add(courses['UniqueID'])
			course_details[courses['UniqueID']] = details
			course_text[courses['UniqueID']] = courses['Title'] + courses['Description']
			tok = re.findall(r'\w+',course_text[courses['UniqueID']],re.UNICODE)
			tok = [x.lower() for x in tok]
			tf_add(tok,courses['UniqueID'])
			idf_add(tok)
		
def clustering():
	global centroid
	global clusters
	for c in clusters:
		if len(c) == 0:
			continue
		for course in clusters[c]:
			for terms in course_tfidf[course]:
				centroid[c][terms] += course_tfidf[course][terms]
		for t in centroid[c]:
			centroid[c][t] = centroid[c][t] / len(c)
			 
	
def process_query(q):
    global query
    global course_idf
    query.clear()
    tok = re.findall(r'\w+',q,re.UNICODE)
    tok = [x.lower() for x in tok]
    for word in tok:
        query[word] += 1
    norm = 0
    for key in query:
        val = query[key]
    	if key in course_idf:
	    	query[key] = (1 + math.log(val,2)) * course_idf[key]
	    	norm += query[key] * query[key]
    norm = math.sqrt(norm)
    if norm !=0 :
        for key in query:
            query[key] /= norm
        
def find_dist(a, b):
    dist = 0.0
    for term in a:
        if term in b:
            dist += a[term] * b[term]
    return dist


def find_closest_cluster():
    global query
    global centroids
    global clusters
    d_list = []
    for c in centroid:
        d = find_dist(centroid[c], query)
        d_list.append((c, d))
    d_list.sort(key=lambda x: x[1], reverse = True)
    return d_list

def search():
	global query
	global course_tfidf
	global q_result
	global course_text
	q_result.clear()
	final_result = []
	d_list = find_closest_cluster()
	cnt = 1
	for c in d_list:
		for doc in clusters[c[0]]:
			for key in query:
				if course_tfidf[doc][key] != 0:
					q_result[doc] += query[key] * course_tfidf[doc][key]
		results= sorted(q_result.items(), reverse = True, key=lambda x : x[1])
		for r in results:
			if r[0] not in final_result:
				final_result.append(r[0])
		results = []

	details_course = []
	for r in final_result[0:5]:
		details_course.append(course_details[r])
	return details_course

def preprocess():
	process_json()
	calc_idf()
	calc_tfidf()
	clustering()
	
def work(query):
	process_query(query)
	p = search()
	return p



    
