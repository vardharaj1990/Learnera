import json
import os
import sys
from collections import defaultdict
import operator
import re
import math
import requests
import random

def dump_json(jfile):
	f = open('mit_ocw.json','a')
	json.dump(jfile, f)
	f.write('\n')
	f.close()

def read_file():		
	f = open('mit_ocw.json','r')
	lines = f.readlines()
	line_num = 0
	for line in lines:
		json_data = json.loads(line)
		for data in json_data['Results']:
			line_num += 1
		print "lines: ", line_num
	f.close()


def main():
	url = 'http://www.ocwsearch.com/api/v1/metadata.json?contact=http%3a%2f%2fwww.ocwsearch.com%2fabout&page='
	read_file()
	'''
	for i in range(1,26):
		furl = url + str(25)
		print furl
		raw_input()
		res = requests.get(furl).json()
		dump_json(res)	
	'''

if __name__ == "__main__" :
	main()
