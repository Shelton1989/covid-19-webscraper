from bs4 import BeautifulSoup
from datetime import datetime
import requests
import unicodedata
import csv
import psycopg2
import environs

env = environs.Env()
env.read_env()

DB_HOST=env.str('DB_HOST')
DB_NAME=env.str('DB_NAME')
DB_USER=env.str('DB_USER')
DB_PW=env.str('DB_PW')

def write_entry(entry):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PW
        )

        cur = conn.cursor()
        
        if entry:
            countryother = entry[0]
            totalcases = int(entry[1].replace(',', ''))
            newcases = entry[2].replace(',', '')
            totaldeaths = entry[3].replace(',', '')
            newdeaths = entry[4].replace(',', '')
            totalrecovered = entry[5].replace(',', '')
            activecases = entry[6].replace(',', '')
            seriouscritical = entry[7].replace(',', '')
            totcases1mpop = entry[8].replace(',', '')
            deaths1mpop = entry[9].replace(',', '')
            date = datetime.strptime('2020 ' + entry[10], '%Y %b %d').strftime('%Y-%m-%d')
            query = f"INSERT INTO cases (countryother, totalcases, newcases, totaldeaths, " \
                    f"newdeaths, totalrecovered, activecases, seriouscritical, totcases1mpop, " \
                    f"deaths1mpop, firstcase) " \
                    f"VALUES ('{countryother}', '{totalcases}', '{newcases}', '{totaldeaths}', '{newdeaths}', " \
                    f"'{totalrecovered}', '{activecases}', '{seriouscritical}', '{totcases1mpop}', '{deaths1mpop}', '{date}') " \
                    f"ON CONFLICT (countryother) DO UPDATE SET " \
                    f"totalcases='{totalcases}', newcases='{newcases}', totaldeaths='{totaldeaths}', " \
                    f"newdeaths='{newdeaths}', totalrecovered='{totalrecovered}', activecases='{activecases}', " \
                    f"seriouscritical='{seriouscritical}', totcases1mpop='{totcases1mpop}', deaths1mpop='{deaths1mpop}' " \
                    f"WHERE cases.countryother = '{countryother}' RETURNING countryother;"

            cur.execute(query)
            conn.commit()
            results = cur.fetchone()
            print(results)
    except Exception as e:
        print(e)

    finally:
        if (conn):
            cur.close()
            conn.close()


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
        new_entry.append(item.get_text(strip=True).strip('\n').strip().replace(',', ''))
    if "Total:" in new_entry:
        csv_file.close()
        break
    csv_write.writerow(new_entry)
    write_entry(new_entry)