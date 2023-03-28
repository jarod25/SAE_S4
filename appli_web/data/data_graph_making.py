import matplotlib.pyplot as plt
from bokeh.io import output_notebook, output_file

output_notebook()
from appli_web.data.data_cleaning import df


def graphique_barres_empilees():
    consommation_par_annee_filiere = df.groupby(["annee", "filiere"])["consommation"].sum()
    consommation_par_annee_filiere.unstack().plot(kind="bar", stacked=False)
    plt.xlabel("Année")
    plt.ylabel("Consommation")
    plt.title("Consommation d'électricité, d'eau ou de gaz par année et filière")
    output_file("templates/consommation_par_annee_filiere.html")


graphique_barres_empilees()
