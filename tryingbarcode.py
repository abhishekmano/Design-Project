# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2

import requests
from bs4 import BeautifulSoup
import json
 
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

cv2.imshow("Image", image)
cv2.waitKey(0)