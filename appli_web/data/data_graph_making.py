from bokeh.plotting import figure
from bokeh.embed import components
from appli_web.data.data_cleaning import df


def graph():
    consommation_par_annee_filiere = df.groupby(["annee", "filiere"])["consommation"].sum()

    p = figure(x_axis_label="Année", y_axis_label="Consommation", title="Consommation d'électricité, d'eau ou de gaz par année et filière")
    p.vbar(x=consommation_par_annee_filiere.index, top=consommation_par_annee_filiere.values, width=0.9)

    script, div = components(p)

    with open("../templates/graph.html", "w") as f:
        f.write(script)
        f.write(div)

    print("graph.html created")

graph()
