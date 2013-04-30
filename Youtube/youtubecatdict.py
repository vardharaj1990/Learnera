import urllib
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import cPickle as pickle
import json
import urllib2
import simplejson
import codecs

categoryIds  = defaultdict(str)
courserayoutubemap = defaultdict(str)
def getYoutubeData():
    catxml = open('chu.xml')
    catdata = catxml.read()
    catSoup = BeautifulSoup(catdata)

    youtubejson = open('youtube.json','a')
    catcount = 0
    for category in catSoup.find_all('atom:category'):
		catName = category['label']
		catId = "Courses for category " + category['term']
		print catId,
		print catName
		categoryIds[catId] = catName

def printCourseraMap():
	file = open('coursera_categories.txt','r')
	content = file.readlines()
	count = 1;
	youtubecat = ""
	courseracat = ""
	for line in content:
		if count == 1:
			courseracat = line
			count = count + 1
			continue
		elif count == 2:
			youtubecat = line
			print courseracat,
			print youtubecat,
			print categoryIds[youtubecat.strip()]
			courserayoutubemap[courseracat.strip('\n')] = youtubecat.strip()
			count = 1
	
	
	return courserayoutubemap
			
				   
if __name__ == "__main__":
	getYoutubeData()
	printCourseraMap()
	#print categoryIds
