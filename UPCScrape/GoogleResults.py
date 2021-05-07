import requests
from selenium import webdriver
import json
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

search_string = "test"


url = "http://www.google.com/search?q=" + search_string

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver.get(url)
content = driver.page_source.encode('utf-8').strip()
time.sleep(5)

# response = requests.get(url)
soup = BeautifulSoup(content, 'html.parser')
total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False)
results_num = ''.join([num for num in total_results_text if num.isdigit()])
convertedresults = int(results_num)
print(total_results_text)
print(type(results_num))
print(convertedresults)
print(type(convertedresults))
driver.quit()