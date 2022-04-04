import requests
import time
from bs4 import BeautifulSoup

url = 'https://www.gsmarena.com/compare.php3?idPhone1='

phone_ids = []
phone_names = []

for i in range(100, 110):
    time.sleep(30)
    reqs = requests.get(url + str(i))
    soup = BeautifulSoup(reqs.text, 'html.parser')

    title = soup.find('title')
    temp = title.get_text()
    phone_names.append(temp[8:-15])
    print(temp)
    phone_ids.append(i)