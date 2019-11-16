# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2

import requests
from bs4 import BeautifulSoup as bs
import json

import mysql.connector
from mysql.connector import Error
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])
 
# find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)

# loop over the detected barcodes
for barcode in barcodes:
	# extract the bounding box location of the barcode and draw the
	# bounding box surrounding the barcode on the image
	(x, y, w, h) = barcode.rect
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
	# the barcode data is a bytes object so if we want to draw it on
	# our output image we need to convert it to a string first
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type
 
	# draw the barcode data and barcode type on the image
	text = "{} ({})".format(barcodeData, barcodeType)
	cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 2)
 
	# print the barcode type and data to the terminal
	#print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

print ("ISBN is "+ barcodeData)
# show the output image
#cv2.imshow("Image", image)
#cv2.waitKey(0)

url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(barcodeData)

r = requests.get(url)
Data = r.content
parseData = json.loads(Data) 
Details = parseData["items"][0]["volumeInfo"]
Title = Details["title"]
#publisher =Details["publisher"]
Date = Details["publishedDate"]
page = Details["pageCount"]
ISBN13 = Details["industryIdentifiers"][0]["identifier"]
Link = Details["infoLink"]
author = Details["authors"][0]
print ("Name of the Book is "+ Title)
print ("Date of release " + Date)
print ("Number of pages is " , page)


webpage = requests.get(Link)
webcontent = webpage.content
htmlcontent = bs(webcontent, 'html.parser')
prices=[] #values present 
details = [] #what is the value
products = htmlcontent.find('table', {'id': 'metadata_content_table'})
for row in products.find_all('tr'):
        for cells in row.find_all('td',{'class':'metadata_value'}):
            prices.append(cells.text)
        for cells in row.find_all('td',{'class':'metadata_label'}):
            details.append(cells.text)
n = len(prices) 
for i in range(n):
    if details[i]=='Title': 
            t = i    
    elif details[i]=='Authors':
            a = i
    elif details[i]=='ISBN':
            id = i
    elif details[i] =='Publisher':
            p = i
    elif details[i] == 'Length':
            l = i

name = prices[t]
isbn =prices[id]
part = isbn.split(",")
isbn =part[1]
isbn10 =part[0]
isbn =isbn.strip()
publisher =prices[p]
part = publisher.split(",")
publisher = part[0]
year = part[1]
pages = prices[l]
part=pages.split()
pages = part[0]
year =year.strip()
part =name.split(",")    
name = part[0]
name = Title
print "ISBN: ",isbn,"name : ",name,"publisher: ",publisher ,"year: ",year,"pages: ",pages

#'''
try:
        connection = mysql.connector.connect(host='localhost',
                                             database='library',
                                             user='root',
                                             password='password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            sql = """INSERT INTO Books( ISBN ,Title,publisher,year,pages ) VALUES (%s,%s,%s,%s,%s)"""
        #try:
            # Execute the SQL command
        recordTuple = ( isbn,name,publisher,year,pages )
        cursor.execute(sql,recordTuple)
        print "Data Successfully added"
            # Commit your changes in the database
        connection.commit()
        #except:
            #print "couldnt"
            # Rollback in case there is any error
            #connection.rollback()
except Error as e:
        print("Error while connecting to MySQL", e)
finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
#'''

#cv2.imshow("Image", image)
#cv2.waitKey(0)