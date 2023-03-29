import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.palettes import Category10
from bokeh.transform import cumsum
from math import pi

from appli_web.data.data_cleaning import df



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

    top10 = df.groupby("libelle_region")["consommation"].sum()
    df_top10 = df[df["libelle_region"].isin(top10.index)]

    df_elec = df_top10[df_top10['filiere'] == 'Electricité'].groupby('libelle_region').sum(numeric_only=True).sort_values(by='consommation', ascending=False)[:10]
    source_elec = ColumnDataSource(df_elec)
    p_elec = figure(y_range=df_elec.index.tolist()[::-1], width=400, height=400, title="Electricité")
    p_elec.hbar(y='libelle_region', right='consommation', height=0.8, source=source_elec)

    df_eau = df_top10[df_top10['filiere'] == 'Eau'].groupby('libelle_region').sum(numeric_only=True).sort_values(by='consommation', ascending=False)[:10]
    source_eau = ColumnDataSource(df_eau)
    p_eau = figure(y_range=df_eau.index.tolist()[::-1], width=400, height=400, title="Eau")
    p_eau.hbar(y='libelle_region', right='consommation', height=0.8, source=source_eau)

    df_gaz = df_top10[df_top10['filiere'] == 'Gaz'].groupby('libelle_region').sum(numeric_only=True).sort_values(by='consommation', ascending=False)[:10]
    source_gaz = ColumnDataSource(df_gaz)
    p_gaz = figure(y_range=df_gaz.index.tolist()[::-1], width=400, height=400, title="Gaz")
    p_gaz.hbar(y='libelle_region', right='consommation', height=0.8, source=source_gaz)

    grid = gridplot([[p_elec, p_eau, p_gaz]])
    output_file("templates/consommation_top10.html")
    save(grid)


def graph_camembert_consomation_totale():
    consommation_totale = df.groupby("filiere")["consommation"].sum()
    source = pd.DataFrame({'filiere': consommation_totale.index, 'consommation': consommation_totale.values})
    graph = figure(height=500, width=500, title='Répartition de la consommation d\'énergie en France',
                   toolbar_location=None,
                   tools="hover", tooltips="@filiere: @consommation_par_filiere")
    graph.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angles', include_zero=True), end_angle=cumsum('angles'),
                    legend_field='filiere', source=source)
    graph.axis.axis_label = None
    graph.axis.visible = False
    graph.grid.grid_line_color = None
    output_file("templates/consommation_camembert.html")
    save(graph)