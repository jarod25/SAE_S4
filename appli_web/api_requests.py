import pandas as pd


def first_request():
    req = pd.read_excel(
        'https://static.data.gouv.fr/resources/arretes-de-catastrophe-naturelle-en-france-metropolitaine-2/20160101-200656/Arretes_de_catastrophe_naturelles.xlsx'
    ).to_json(
        orient='records'
    )
    print(req)
    return req


first_request()


def second_request():
    req = pd.read_xml('https://georisques.gouv.fr/services').to_json(orient='records')
    print("Deuxième requête !")
    return req
