import pandas as pd
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


ID_And_UPC_Dict = {"AA15Volt" : None}






url = "https://www.womacktools.com/aa-15-volt-pc1500-procell-alkaline-battery/product/0/76534"

UPCs = []

# response = requests.get(url)
#here's where idk what I'm doing?
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
text =  soup.get_text()
# #probably need and if then pass
# UPCs.append()
# ID_And_UPC_Dict[ItemID[i]] = UPCs
string = text.find('UPC')
string_end = string + 30
Code = text[string:string_end]
CleanCode = ''.join([num for num in Code if num.isdigit()])
UPCs.append(Code)
UPCs.append(CleanCode)
ID_And_UPC_Dict["AA15Volt"] =  UPCs
print(Code)
print(CleanCode)
print(ID_And_UPC_Dict)

df2 = pd.DataFrame(data=ID_And_UPC_Dict)
df2.to_excel('C:/Users/aeaker/Documents/VSC/UPCScrape/dict1.xlsx', index=False)