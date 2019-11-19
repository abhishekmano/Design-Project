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

a = raw_input("Show Book") 

bgr = (8, 70, 208)

cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    data,flag = barcodeReader(frame, bgr)
    #print(barcode)
    if(flag==1):
        print(data)
        cv2.destroyWindow('Barcode reader')
        cap.release()
        break
    cv2.imshow('Barcode reader', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break

a = raw_input("Show ID") 

bgr = (8, 70, 208)

cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    id,flag = barcodeReader(frame, bgr)
    #print(barcode)
    if(flag==1):
        print(id)
        cv2.destroyWindow('Barcode reader')
        break
    cv2.imshow('Barcode reader', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
try:
        connection = mysql.connector.connect(host='localhost',
                                             database='library',
                                             user='root',
                                             password='password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            #print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            sql = """INSERT INTO issue(ISBN , adm_no ) VALUES (%s,%s)"""
        #try:
            # Execute the SQL command
        recordTuple = (data, id )
        cursor.execute(sql,recordTuple)
        print "Data Successfully added"+ data + " " + id
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