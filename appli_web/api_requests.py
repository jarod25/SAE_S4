import pandas as pd
import requests


def first_request():
    req = requests.get(
        'https://odre.opendatasoft.com/api/records/1.0/search/?dataset=temperature-quotidienne-departementale&q=&facet=date_obs&facet=departement&refine.date_obs=2023'
    ).json()
    print("Première Requête !")
    return req


def second_request():
    req = requests.get(
        'https://odre.opendatasoft.com/api/records/1.0/search/?dataset=prod-nat-gaz-horaire-prov&q=&facet=journee_gaziere&facet=operateur'
    ).json()
    print("Deuxième requête !")
    return req
