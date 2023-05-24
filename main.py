import csv
import requests
import time
from random import randrange

# GLOBAL VARIABLES
PATH_FILE = 'people.csv'
URL_API = 'https://legalizacionservice.mescyt.gob.do/api/legalizaciones/getall/'
SKIP_FIRRT_LINE = True
PEOPLES = []
RES_DATA = []


def get_random_time_sleep():
    time_travel = randrange(100, 200) / 1000.0
    return time_travel


# open file and read
with open(PATH_FILE, 'r') as csv_file:
    # Skip first line
    if SKIP_FIRRT_LINE:
        next(csv_file)

    reader_csv = csv.reader(csv_file, delimiter=',')
    for row in reader_csv:
        # if row is empty then skip
        if len(row) == 0:
            continue

        people = {
            'DNI': row[0].replace('-', ''),
            'NAME': row[1],
            'LAST_NAME_1': row[2],
            'LAST_NAME_2': row[3],
        }
        PEOPLES.append(people)
csv_file.close()

# fetch data from csv_data
for index, people in enumerate(PEOPLES):
    time.sleep(get_random_time_sleep())
    response = requests.get(URL_API + people['DNI'])

    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            RES_DATA.append(data[0])
        else:
            RES_DATA.append({
                'solicitante': people['NAME'] + ' ' + people['LAST_NAME_1'] + ' ' + people['LAST_NAME_2'],
                # 'solicitante': people['NAME'],
                'estado': 'NO ENCONTRADO',
                'observacion': 'NO ENCONTRADO',
                'ies': []
            })

# write data in txt file
with open('res.txt', 'a') as file:
    for data in RES_DATA:
        print(data)
        file.write('####################\n')
        file.write(
            'NAME: ' + str(data['solicitante']) + '\n' +
            'STATE: ' + str(data['estado']) + '\n' +
            'NOTE: ' + str(data['observacion']) + '\n'
        )

        # for every document
        for document in data['ies']:
            file.write(
                'UNIVERSITY: ' + document['descripcion'] + '\n' +
                'CAREER: ' + document['carrera'] + '\n'
            )

        file.write('####################\n')
        file.write('\n')
file.close()
