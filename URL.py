import requests
from bs4 import BeautifulSoup as bs
import mysql.connector
from mysql.connector import Error
a=raw_input("Enter the URL: ")
webpage = requests.get(a)
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