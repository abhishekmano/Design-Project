import requests
from bs4 import BeautifulSoup as bs
webpage = requests.get("https://books.google.co.in/books?vid=isbn9788120301450&redir_esc=y&hl=en")
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
        
        
print prices
print details

#df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
#df.to_csv('products.csv', index=False, encoding='utf-8')