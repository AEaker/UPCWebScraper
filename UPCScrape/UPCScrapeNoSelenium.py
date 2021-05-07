import csv
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
from random import randint
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--ignore-ssl-errors')
# #chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--incognito")

# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

headers = {
  'user-agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36'}

# driver.set_page_load_timeout(10)

ID_And_UPC_Dict = {}

links = [] 

#Excel with part info
df = pd.read_excel("ScrapeTest.xlsx", 'Sheet2')

# for index, row in df.iterrows():
#     search_string = row["Item ID"].replace(' ', '+') + "+" + row["Description"].replace(' ','+')

ItemID = df.iloc[0:,0]
for i in range(0, len(df)):
    #make google query from item id and description
    search_string = df.iloc[i]["Item ID"].replace(' ', '+') + "+" + df.iloc[i]["Description"].replace(' ','+')
    #reset codes
    UPCs = []
    links = []
    ID_And_UPC_Dict[ItemID[i]] = None
    print('Researching #' + str(i) +' out of ' + str(len(df)))
    url = "http://www.google.com/search?q=" + search_string
    response = requests.get(url, headers=headers, timeout=12)
    # content = driver.page_source.encode('utf-8').strip()
    time.sleep(randint(2, 10))
    soup = BeautifulSoup(response.text, 'html.parser')
    total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False)
    results_num = ''.join([num for num in total_results_text if num.isdigit()])
    try:
        convertedresults = int(results_num)
        if convertedresults > 10:
            n_pages = 2
            for page in range(1, n_pages):
                url = "http://www.google.com/search?q=" + search_string + "&start=" +  str((page - 1) * 10)
                response = requests.get(url, headers=headers, timeout=12)
                time.sleep(randint(2, 10))
                soup = BeautifulSoup(response.text, 'html.parser')
                # soup = BeautifulSoup(r.text, 'html.parser')
                linksearch = soup.find_all('div', class_="yuRUbf")
                print('Grabbing links...')
                for data in linksearch:
                    links.append(data.a.get('href'))    

                for link in links:
                    try:
                        response.get(link)
                        #response = requests.get(link, headers=headers, timeout=12)
                        time.sleep(randint(2, 10))
                        soup = BeautifulSoup(response.text, 'html.parser')
                        text =  soup.get_text()
                        print('Searching for data on ' + link)
                        #If UPC is on the page, grab it, if not, move on.
                        if text.find('UPC') != -1:
                            print('UPC found..adding to list..')
                            string = text.find('UPC')
                            string_end = string + 30
                            Code = text[string:string_end]
                            CleanCode = ''.join([num for num in Code if num.isdigit()])
                            UPCs.append(CleanCode) 
                        else:
                            print("No UPC found, moving to next link.")
                    except (TimeoutException, WebDriverException):
                        print("Connection Timed Out")
                        continue
                    # except requests.Timeout:
                    #     pass
                    # except requests.exceptions.ConnectionError:
                    #     print("Connection Reset Error")
        elif convertedresults == None:
            continue
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            linksearch = soup.find_all('div', class_="yuRUbf")
            print('Grabbing links...')
            for data in linksearch:
                links.append(data.a.get('href'))    

            for link in links:
                try:
                    response = requests.get(url)
                    #response = requests.get(link, headers=headers, timeout=12)
                    time.sleep(randint(2, 10))
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text =  soup.get_text()
                    print('Searching for data on ' + link)
                    #If UPC is on the page, grab it, if not, move on.
                    if text.find('UPC') != -1:
                        print('UPC found..adding to list..')
                        string = text.find('UPC')
                        string_end = string + 30
                        Code = text[string:string_end]
                        CleanCode = ''.join([num for num in Code if num.isdigit()])
                        UPCs.append(CleanCode) 
                    else:
                        print("No UPC found, moving to next link.")
                # except TimeoutException:
                #     print("Connection Timed Out")
                except requests.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    print("Connection Reset Error")
    except TypeError:
        pass
   
        
    ID_And_UPC_Dict[ItemID[i]] = UPCs


# with open('IDUPCDict.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     for key, value in ID_And_UPC_Dict.items():
#         writer.writerow([key, value])

driver.quit()
while True:
    try:
        ID_UPC = pd.DataFrame(data=ID_And_UPC_Dict)
        ID_UPC.to_excel('C:/Users/aeaker/Documents/VSC/UPCScrape/UPC.xlsx')
    except:
        print("Couldn't write excel file....")
        continue

    try:
        with open('IDUPCDict1.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for key, values in ID_And_UPC_Dict.items():
                for value in values:
                    writer.writerow([key, value])
    except:
        print("Couldn't write csv file....")
        continue


print('-------------------------------')
print(links)
print('-------------------------------')
print(ID_And_UPC_Dict)