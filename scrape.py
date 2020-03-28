from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.worldometers.info/coronavirus/#countries').text


soup = BeautifulSoup(source, 'lxml')

print(soup)