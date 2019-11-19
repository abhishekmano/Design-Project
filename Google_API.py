import requests
from bs4 import BeautifulSoup
import json

#a= input ("Enter ISBN")
url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(9780131593183)

r = requests.get(url)
Data = r.content
parseData = json.loads(Data) 
Details = parseData["items"][0]["volumeInfo"]
Title = Details["title"]
publisher =Details["publisher"]
Date = Details["publishedDate"]
page = Details["pageCount"]
ISBN13 = Details["industryIdentifiers"][0]["identifier"]
Link = Details["infoLink"]
author = Details["authors"][0]
print ("Name of the Book is "+ Title)
print (publisher)
print ("Date of release " + Date)