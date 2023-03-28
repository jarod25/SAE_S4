import pandas as pd
import requests

# Récupération des données locales depuis le dossier json_csv_files

elec_et_gaz = pd.read_json('json_csv_files/conso-elec-gaz-annuelle-par-naf-agregee-departement.json')
eau2015 = pd.read_csv('json_csv_files/eau2015.csv', low_memory=False)
eau2016 = pd.read_csv('json_csv_files/eau2016.csv', low_memory=False)
eau2017 = pd.read_csv('json_csv_files/eau2017.csv', low_memory=False)
eau2018 = pd.read_csv('json_csv_files/eau2018.csv', low_memory=False)
eau2019 = pd.read_csv('json_csv_files/eau2019.csv', low_memory=False)
eau2020 = pd.read_csv('json_csv_files/eau2020.csv', low_memory=False)
eau2021 = pd.read_csv('json_csv_files/eau2021.csv', low_memory=False)

# Récupération des données de l'API

elec_part1 = 'https://odre.opendatasoft.com/api/records/1.0/search/?dataset=soutirages-regionaux-quotidiens-provisoires-rpt&q=date%3A%5B2022-10-07+TO+2023-03-16%5D&rows=-1&sort=date'
elec_part2 = 'https://odre.opendatasoft.com/api/records/1.0/search/?dataset=soutirages-regionaux-quotidiens-provisoires-rpt&q=date%3A%5B2022-04-23+TO+2022-10-06%5D&rows=-1&sort=date'
elec_part3 = 'https://odre.opendatasoft.com/api/records/1.0/search/?dataset=soutirages-regionaux-quotidiens-provisoires-rpt&q=date%3A%5B2022-01-01+TO+2022-04-22%5D&rows=-1&sort=date&refine.date=2022'
elec = []

urls = [elec_part1, elec_part2, elec_part3]

for url in urls:
    data = requests.get(url).json()
    elec.extend(data['records'])

gaz1 = 'https://odre.opendatasoft.com/api/records/1.0/search/?dataset=consommation-maximale-horaire-de-gaz-par-jour-a-la-maille-regional&q=&rows=-1&refine.date=2023'
gaz2 = 'https://odre.opendatasoft.com/api/records/1.0/search/?dataset=consommation-maximale-horaire-de-gaz-par-jour-a-la-maille-regional&q=&rows=-1&refine.date=2022'
gaz = []

urls2 = [gaz1, gaz2]

for url2 in urls2:
    data = requests.get(url2).json()
    gaz.extend(data['records'])
