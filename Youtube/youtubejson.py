import urllib
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import cPickle as pickle
import json
import urllib2
import simplejson

def deflist():
	return defaultdict(list)

categories = defaultdict(deflist)
categoryMap = defaultdict(list)
categoryIds  = defaultdict(str)



def getYoutubeData():
        catxml = open('chu.xml')
        catdata = catxml.read()
        catSoup = BeautifulSoup(catdata)
        #try1 = 'catSoup.app:categories'

        youtubejson = open('youtube.json','a')
        catcount = 0
        for category in catSoup.find_all('atom:category'):
            catName = category['label']
            catId = category['term']

            print catId,
            print catName           
            
            parent = category.find_all('yt:parentcategory')[0]['term']
            if not categoryMap[parent]:
                categoryMap[parent] = list()
            categoryMap[parent].append(catId)
            
            caturl = 'http://gdata.youtube.com/feeds/api/edu/courses?category=' + catId  +  '&alt=json&prettyprint=true&v=2'
            r = urllib2.Request(caturl)
            opener = urllib2.build_opener()
            f = opener.open(r)
            data = simplejson.load(f)
            key = 'entry'
            json.dump(data, youtubejson)
            youtubejson.write('\n')
            if key in data['feed']:     
                    for entry in data['feed']['entry']:
                            title = entry['title']['$t']
                            summary = entry['summary']['$t']
                            plid = entry['yt$playlistId']['$t']
                            playlistlink = 'http://www.youtube.com/playlist?list=' + plid
                            courseData = list()
                            courseData.append(title)
                            courseData.append(summary)
                            courseData.append(playlistlink)
                            categories[catName][plid] = courseData

            catcount = catcount  + 1
            
        youtubejson.close()
        pickle.dump( categories, open( "youtube.p", "wb" ) )
            

def getYoutubeDataDict():
        return  pickle.load(open( "./youtube.p", "rb" ) )
        
        


if __name__ == "__main__":
         #print getYoutubeDataDict()
         getYoutubeData()
         #f = open('youtube.txt','r')
         
         #my_dict = literal_eval(f.read())
         #getYoutubeDataDict()
         '''
         my_dict = getYoutubeDataDict()
         count = 0
         for cat in my_dict:
                print cat
                print my_dict[cat]
         '''
       
	
