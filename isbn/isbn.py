import urllib
import re
from bs4 import BeautifulSoup


def getisbnData(query):
	keywords = re.split(r"[\W]+",query)
	value = ''
	i = 0
	size = len(keywords)
	while i < size:
		if i==0:
			value = keywords[i]
		else:
			value = value + '+' +  keywords[i]
		i = i + 1

	isbnurl = 'https://isbndb.com/api/books.xml?access_key=IMHDRIT9&index1=title&value1=' + value

  	r = urllib.urlopen(isbnurl)
  	isbn = BeautifulSoup(r)
  	booksdata = isbn.isbndb.booklist


if __name__ == "__main__":
	 getisbnData('the theif of time')
	
