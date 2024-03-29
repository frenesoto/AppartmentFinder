#! python3
import requests as r
from bs4 import BeautifulSoup as bs
import webbrowser as w
from openpyxl import Workbook as book
from plyer import notification as noti
from datetime import date

filename = "Apartment.xlsx"#This creates the excel spreadsheet each time
workbook = book()
sheet = workbook.active
c = 0#this is a counter for looping through the URL's in the list
li = []#records links to rentals so that no repeats come up
URL = ['https://sfbay.craigslist.org/search/apa?sort=date&availabilityMode=0&postal=94521&search_distance=20']
Lis = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
today =date.today()
o=1
for i in URL:#This cycles through the URL's if you have more than one
    page = r.get(URL[c])
    c+=1
    #print("\n" + '>' + (URL[c])) #Because adding it to the print above would not work
    soup = bs(page.content, "html.parser")#parses the html
    searc = soup.find(id="searchform")#This selects all info on the page
    rent = searc.find_all("li", class_="result-row") #this defines the information for each item on the page   
    for x in rent:
        itemname = x.find("a", class_= "result-title hdrlnk")
        price = x.find("span", class_= "result-price")
        location = x.find("span", class_= "result-hood")
        linker = x.find("a", class_= "result-title hdrlnk")
        posted = x.find("time", class_="result-date")
        if itemname not in li:
            if location is not None:
                if (int(price.text.replace('$', '').replace(',','')) <= 8000)and (int(price.text.replace('$', '').replace(',','')) >= 10): #Keeps the apartments pulled in a range
                    li.append(linker["href"])
                    o+=1 #This helps to move to the next line on the sheet with each new entry
                    sheet['A1'] = 'Item Name' ;sheet['E1'] = 'Posted';sheet['B1'] = 'Price' ;sheet['C1'] = 'Link' ;sheet['D1'] = 'Location' ;
                    sheet.column_dimensions['A'].width = 63;sheet.column_dimensions['C'].width = 89;sheet.column_dimensions['D'].width = 29 
                    sheet['A'+str(o)] = str(itemname.text)
                    sheet['B'+str(o)] = str(price.text)
                    sheet['C'+str(o)] = str(linker["href"])
                    sheet['D'+str(o)] = str(location.text)
                    sheet['E'+str(o)] = str(posted.text)
                    workbook.save(filename = filename)