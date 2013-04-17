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
courses_tf = defaultdict(func)
courses_idf = defaultdict(func)
clusters = defaultdict(set)
course_text = defaultdict(str)
course_cat = defaultdict(set)
course_tfidf = defaultdict(func2)

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
        print 'Done'
    f.close()

def tf_add(tok,d_id):
    global course_tf
    for word in tok:
        course_tf[d_id][word] += 1
    for word in tok:
        val = course_tf[d_id][word]
        course_tf[d_id][word] = 1 + math.log(val,2)

def idf_add(tok,cat_id):
    global course_idf
    tok_s = set(tok)
    for word in tok_s:
        course_idf[cat_id][word] += 1

def calc_idf():
    global course_idf
    global num_docs
    for key in course_idf:
        course_idf[key] = math.log((float(num_docs)/course_idf[key]),2)

def calc_tfidf():
    global course_idf
    global course_tf
    global course_tfidf

    for doc_id in course_tf:
        norm = 0
        for cat in course_cat[doc_id]:
            for term in course_tf[doc_id]:
                course_tf[doc_id][term] = course_tf[doc_id][term] * course_idf[term]
                norm += course_tf[doc_id][term] * course_tf[doc_id][term]
                norm = math.sqrt(norm)
        for term in course_tf[doc_id]:
            course_tf[doc_id][term] = course_tf[doc_id][term] / norm

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
        r = json.loads(line)
        for course in r:
            course_text[course['short_name']] = course['about_the_course']
            course_text[course['short_name']] += course['short_description'] + course['description']
            course_text[course['short_name']] = re.sub('<[^<]+?>|\\n', ' ', course_text[course['short_name']])
            tok = re.findall(r'\w+',course_text[course['short_name']],re.UNICODE)
            tf_add(tok,course['short_name'])
            for id in course['category-ids']:
                idf_add(tok,id)

def print_courses():
    sc = 0
    sn = 0
    print 'Total number of courses: ', num_courses
    print 'links: ', len(links)
    for i in social_links:
        if i != 'null':
            print i
            sc += 1
    print sc
    print num_courses
    for i in short_names:
        if i!= 'null':
            sn += 1 
            print i
    print 'short names: ' 
    print clusters
    '''
    for i in links:
        print i
        '''

def main():
    #read_json()
    #read_json2()
    
    process_json()
    #read_course_json()
    process_courses()
    #print_courses()
    raw_input()

if __name__ == '__main__':
    main()

    