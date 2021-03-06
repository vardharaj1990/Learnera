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
short_names = set()
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
    f = open("fullcourses.txt", 'rU')
    content = f.readlines()
    for line in content:
        r = json.loads(line)
        for courses in r:
            num_courses += 1
            social_links.add(courses['social_link'])
            short_names.add(courses['short_name'])
            for cat in courses['category-ids']:
                clusters[cat].add(courses['short_name'])
                course_cat[courses['short_name']].add(cat)
            for course in courses['courses']:
                links.add(course['home_link'])

def process_courses():
	f = open("courses.txt", 'rU')
	content = f.readlines()
	for line in content:
		course = json.loads(line)
		course_text[course['short_name']] = course['name']
		course_text[course['short_name']] += course['about_the_course']
		course_text[course['short_name']] += course['short_description'] + course['description']
		course_text[course['short_name']] = re.sub('<[^<]+?>|\\n', ' ', course_text[course['short_name']])
		tok = re.findall(r'\w+',course_text[course['short_name']],re.UNICODE)
		tok = [x.lower() for x in tok]
		tf_add(tok,course['short_name'])
		idf_add(tok)
		details = []
		details.append(course['short_name'])
		details.append(course['name'])
		details.append(course['short_description'])
		details.append(course['universities'][0]['name'])
		details.append(course['small_icon_hover'])
		details.append(course['instructor'])
		details.append(course['courses'][len(course['courses']) - 1]['duration_string'])
		details.append(course['courses'][len(course['courses']) - 1]['start_date_string'])
		course_details[course['short_name']] = details
		
def clustering():
	global centroid
	for c in clusters:
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
	for r in final_result[0:10]:
		details_course.append(course_details[r])
	return details_course

def preprocess():
	process_json()
	process_courses()
	calc_idf()
	calc_tfidf()
	clustering()
	
def work(query):
	process_query(query)
	p = search()
	return p



    
