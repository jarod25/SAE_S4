import pandas as pd
from appli_web.data import data_loading

# Récupération des données depuis data_loading.py
elec_et_gaz = data_loading.elec_et_gaz
eau2015 = data_loading.eau2015
eau2016 = data_loading.eau2016
eau2017 = data_loading.eau2017
eau2018 = data_loading.eau2018
eau2019 = data_loading.eau2019
eau2020 = data_loading.eau2020
eau2021 = data_loading.eau2021
elec = data_loading.elec
gaz = data_loading.gaz

# Nettoyage df_elec_et_gaz
df_elec_et_gaz = elec_et_gaz.loc[:, ['conso', 'annee', 'filiere', 'libelle_region']]
df_elec_et_gaz = df_elec_et_gaz.rename(columns={'conso': 'consommation'})

# Nettoyage df_eau
df_eau_concat = pd.concat([eau2015, eau2016, eau2017, eau2018, eau2019], axis=0, keys='annee')
df_eau_concat2 = pd.concat([eau2020, eau2021], axis=0, keys='annee')
df_eau = pd.concat([df_eau_concat, df_eau_concat2], axis=0, keys='annee')
df_eau = df_eau.loc[:, ['Année', 'Volume (m3)', 'Département']]
df_eau = df_eau.rename(columns={'Année': 'annee', 'Volume (m3)': 'consommation'})
df_eau = df_eau.assign(filiere=['Eau'] * len(df_eau))

# Fonction pour transformer départements en régions
DEPS_TO_REGS = {
    ('1', '3', '7', '01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'): 'Auvergne-Rhône-Alpes',
    ('9', '09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'): 'Occitanie',
    ('14', '27', '50', '61', '76'): 'Normandie',
    ('2', '02', '59', '60', '62', '80'): 'Hauts-de-France',
    ('16', '17', '79', '86', '19', '23', '87', '24', '33', '40', '47', '64'): 'Nouvelle-Aquitaine',
    ('18', '28', '36', '37', '41', '45'): 'Centre-Val de Loire',
    ('8', '08', '10', '51', '52', '54', '55', '57', '67', '68', '88'): 'Grand Est',
    ('22', '29', '35', '56'): 'Bretagne',
    ('25', '39', '70', '90', '21', '71', '58', '89'): 'Bourgogne-Franche-Comté',
    ('44', '49', '53', '72', '85'): 'Pays de la Loire',
    ('4', '5', '6', '04', '05', '06', '13', '83', '84'): 'Provence-Alpes-Côte d\'Azur',
    ('2A', '2B'): 'Corse',
    ('75', '77', '78', '91', '92', '93', '94', '95'): 'Île-de-France',
    '971': 'Guadeloupe',
    ('972', '972R'): 'Martinique',
    ('973', '973R'): 'Guyane',
    '974': 'La Réunion',
    ('976', '976D'): 'Mayotte'
}

def dep_to_reg(num_departement) -> str:
    for liste_num_departements, nom_region in DEPS_TO_REGS.items():
        if str(num_departement) in liste_num_departements:
            return nom_region


# Ajouter colonne "region" au dataframe eau
df_eau['libelle_region'] = df_eau['Département'].apply(dep_to_reg)
df_eau = df_eau.dropna()

# Garder seulement les colonnes nécessaires
df_eau = df_eau.loc[:, ['annee', 'consommation', 'libelle_region', 'filiere']]

# Nettoyage de l'electricité 2022 - 2023
df_elec = pd.json_normalize(elec)
df_elec = df_elec.loc[:, ['fields.energie_journaliere', 'fields.date', 'fields.region']]
df_elec = df_elec.rename(
    columns={'fields.energie_journaliere': 'consommation', 'fields.date': 'annee', 'fields.region': 'libelle_region'})
df_elec['annee'] = pd.to_datetime(df_elec['annee'])
df_elec['date'] = df_elec['annee'].dt.date  # extraire la date sans l'année
df_elec['annee'] = df_elec['annee'].dt.year  # extraire l'année
df_elec = df_elec.groupby(['annee', 'libelle_region'], as_index=False)['consommation'].sum()
df_elec['consommation'] = df_elec['consommation'].apply(int)
df_elec = df_elec.assign(filiere=['Electricité'] * len(df_elec))

# Nettoyage du gaz pour 2022 - 2023
df_gaz = pd.json_normalize(gaz)
df_gaz = df_gaz.loc[:, ['fields.date', 'fields.nom_officiel_region', 'fields.consommation_maximale_mwh']]
df_gaz = df_gaz.rename(columns={'fields.date': 'annee', 'fields.nom_officiel_region': 'libelle_region',
                                'fields.consommation_maximale_mwh': 'consommation'})
df_gaz['annee'] = pd.to_datetime(df_gaz['annee'])
df_gaz['date'] = df_gaz['annee'].dt.date  # extraire la date sans l'année
df_gaz['annee'] = df_gaz['annee'].dt.year  # extraire l'année
df_gaz = df_gaz.groupby(['annee', 'libelle_region'], as_index=False)['consommation'].sum()
df_gaz['consommation'] = df_gaz['consommation'].apply(int)
df_gaz = df_gaz.assign(filiere=['Gaz'] * len(df_gaz))

# Fusion des df

df_elec_et_gaz = df_elec_et_gaz.reset_index()
df_gaz = df_gaz.reset_index()
df_elec = df_elec.reset_index()
df_eau = df_eau.reset_index()

# Conversion de M³ en MW
df_eau["consommation"] = df_eau["consommation"] * 0.01055 / 10

df_concat = pd.concat([df_elec_et_gaz, df_gaz, df_elec, df_eau], axis=0, keys='annee')
df_concat['annee'] = df_concat['annee'].astype(int)
df = df_concat.sort_values(by='annee')
df = df[df.annee >= 2014]

df = df.drop('level_0', axis=1)
df = df.drop('level_1', axis=1)
df = df.drop('level_2', axis=1)