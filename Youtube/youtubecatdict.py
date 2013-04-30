import urllib
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import cPickle as pickle
import json
import urllib2
import simplejson
import codecs

courserayoutubemap = defaultdict(str)

def getCourseraMap():
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
			
