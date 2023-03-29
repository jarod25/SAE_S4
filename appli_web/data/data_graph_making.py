from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10_10
from appli_web.data.data_cleaning import df


def graph():
    fig = figure(title='test', x_axis_label='annee', y_axis_label='consommation')
    fig.line(df['annee'], df['consommation'], line_width=2)
    output_file('templates/graph.html')
    save(fig)

def graph_elec_consommation():
    consommation_elec = df[df["filiere"] == "Electricité"].groupby("annee")["consommation"].sum()
    fig = figure(x_axis_label='annee', y_axis_label='consommation')
    fig.line(consommation_elec.index, consommation_elec.values, line_width=2)
    output_file('templates/consommation_elec.html')
    save(fig)

def graph_gaz_consommation():
    consommation_gaz = df[df["filiere"] == "Gaz"].groupby("annee")["consommation"].sum()
    fig = figure(x_axis_label='annee', y_axis_label='consommation')
    fig.line(consommation_gaz.index, consommation_gaz.values, line_width=2)
    output_file('templates/consommation_gaz.html')
    save(fig)

def graph_eau_consommation():
    consommation_eau = df[df["filiere"] == "Eau"].groupby("annee")["consommation"].sum()
    fig = figure(x_axis_label='annee', y_axis_label='consommation')
    fig.line(consommation_eau.index, consommation_eau.values, line_width=2)
    output_file('templates/consommation_eau.html')
    save(fig)

def graph_top10():
    # Génère moi un graphique des 10 régions qui consommes le plus au total (tous les années confondues) avec Bokeh
    # 1. On récupère les 10 régions qui consomment le plus
    top10 = df.groupby("libelle_region")["consommation"].sum().sort_values(ascending=False).head(10)
    # 2. On récupère les données de consommation de ces 10 régions
    top10_data = df[df["libelle_region"].isin(top10.index)]
    # 3. On crée un graphique avec Bokeh
    fig = figure(x_axis_label='annee', y_axis_label='consommation', title="Top 10 des régions qui consomment le plus")
    # 4. On crée une palette de couleur
    palette = Category10_10
    # 5. On crée une source de données
    source = ColumnDataSource(top10_data)
    # 6. On crée une boucle pour afficher les 10 régions
    for i, region in enumerate(top10.index):
        fig.line(x="annee", y="consommation", source=source, color=palette[i], legend_label=region)
    # 7. On ajoute un outil pour afficher les données au survol de la souris
    fig.add_tools(HoverTool(tooltips=[("Région", "@libelle_region"), ("Année", "@annee"), ("Consommation", "@consommation")]))
    # 8. On sauvegarde le graphique
    output_file('templates/consommation_top10.html')
    save(fig)
