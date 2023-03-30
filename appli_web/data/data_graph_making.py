import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import gridplot
from bokeh.palettes import Category10
from bokeh.transform import cumsum
from math import pi
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.models.widgets import Tabs, Panel

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
    data = pd.Series(consommation_totale).reset_index(name='value').rename(columns={'index': 'filiere'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category10[len(data)]

    p = figure(height=350, title="Consommation totale par filière", toolbar_location=None,
            tools="hover", tooltips="@filiere: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='filiere', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    output_file("templates/consommation_camembert.html")
    save(p)


# graphique interactif avec bokeh ou on peut choisir l'année, la filière et la région pour voir la consommation
def graph_interactif():

    # Create Input controls
    annee = Slider(title="Année", value=2014, start=2014, end=2023, step=1)
    filiere = Select(title="Filière", value="Electricité", options=['Electricité', 'Gaz', 'Eau'])
    region = Select(title="Région", value="Auvergne-Rhône-Alpes", options=df['libelle_region'].unique().tolist())

    # Create Column Data Source that will be used by the plot
    source = ColumnDataSource(data=dict(x=[], y=[]))

    # Create the figure
    plot = figure(plot_height=600, plot_width=600, title='Consommation', x_axis_label='Mois', y_axis_label='Consommation')
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

    # Define the callback function: update_plot
    def update_plot(attr, old, new):
        # Get the current slider values
        a = annee.value
        f = filiere.value
        r = region.value

        # Generate the new curve
        x = df[(df['annee'] == a) & (df['filiere'] == f) & (df['libelle_region'] == r)].groupby('mois').sum(numeric_only=True).index.tolist()
        y = df[(df['annee'] == a) & (df['filiere'] == f) & (df['libelle_region'] == r)].groupby('mois').sum(numeric_only=True)['consommation'].tolist()

        new_data = dict(x=x, y=y)
        source.data = new_data

    # Attach the callback to the 'value' property of slider
    annee.on_change('value', update_plot)
    filiere.on_change('value', update_plot)
    region.on_change('value', update_plot)

    # Create a row layout
    layout = column(row(annee, filiere, region), plot)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Consommation')

    # Add the tab to the current document
    curdoc().add_root(layout)

    output_file("templates/consommation_interactif.html")
    save(layout)