from pyzbar.pyzbar import decode
import cv2
import numpy as np

import requests
from bs4 import BeautifulSoup as bs
import json

import mysql.connector
from mysql.connector import Error

flag=0

def barcodeReader(image, bgr):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    for decodedObject in barcodes:
        points = decodedObject.polygon

        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

    for bc in barcodes:
        cv2.putText(frame, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    bgr, 2)
        flag=1
        #print (bc.data)
        return bc.data,flag
    return '',0


bgr = (8, 70, 208)

cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    data,flag = barcodeReader(frame, bgr)
    #print(barcode)
    if(flag==1):
        print(data)
        break
    cv2.imshow('Barcode reader', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break

url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(data)

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
#print ("Name of the Book is "+ Title)
#print ("Date of release " + Date)
#print ("Number of pages is " , page)


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
            sql = """INSERT INTO Books( ISBN ,Title,publisher,year,pages,count ) VALUES (%s,%s,%s,%s,%s,1)"""
        #try:
            # Execute the SQL command
        recordTuple = ( isbn,Title,publisher,year,pages )
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