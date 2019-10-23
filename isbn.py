import requests
from bs4 import BeautifulSoup as bs
import urllib2
#a=raw_input("Enter the URL: ")
webpage = urllib2.urlopen('https://isbnsearch.org/isbn/9780131593183')
htmlcontent = bs(webpage, 'html.parser')
value=[] #values present 
tag = [] #what is the value 
products = htmlcontent.find('div')
print (products)
#for row in products.find_all('tr'):
#        for cells in row.find_all('td',{'class':'metadata_value'}):
#            prices.append(cells.text)
#        for cells in row.find_all('td',{'class':'metadata_label'}):
#            details.append(cells.text)