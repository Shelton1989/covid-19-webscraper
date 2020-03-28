from bs4 import BeautifulSoup
from datetime import datetime
import requests
import unicodedata
import csv

source = requests.get('https://www.worldometers.info/coronavirus/#countries').text

date = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M')

csv_file = open(f'covid-19-data-{date}.csv', 'w')
csv_write = csv.writer(csv_file)

soup = BeautifulSoup(source, 'lxml')

new_headings = []

for heading in soup.find_all("th"):
    new_heading = unicodedata.normalize(
        'NFKD', 
        heading.get_text(strip=True).replace(',', '').replace('/', '')
        ).replace(' ', '').strip('\n')
    if new_heading not in new_headings:
        new_headings.append(new_heading)

csv_write.writerow(new_headings)

dataset = soup.find_all("tr", style="")

for entry in dataset:
    new_entry = []
    for item in entry.find_all("td"):
        new_entry.append(item.get_text(strip=True).strip('\n').strip())
    csv_write.writerow(new_entry)
    if "Total:" in new_entry:
        break

csv_file.close()