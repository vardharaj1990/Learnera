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
  	booksdata = isbn.isbndb.booklist.find_all('bookdata')
        returnBooks = [[] for _ in range(len(booksdata))]
        bookLinkBase = 'https://isbndb.com/d/book/'

        bookCount = 0
        for d in booksdata:
                isbnid = d.get('isbn')
                bookid = d.get('book_id')
                booklink = bookLinkBase + d.get('book_id') + '.html'
                bookTitle = d.title.string
                authorsText = d.authorstext.string
                titleLong = d.titlelong.string
                returnBooks[bookCount].append(isbnid)
                returnBooks[bookCount].append(bookid)
                returnBooks[bookCount].append(booklink)
                returnBooks[bookCount].append(bookTitle)
                returnBooks[bookCount].append(authorsText)
                returnBooks[bookCount].append(titleLong)
                bookCount = bookCount + 1
        
        return returnBooks       
        

if __name__ == "__main__":
	 getisbnData('the theif of time')
	
