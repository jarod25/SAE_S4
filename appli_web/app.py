#! /usr/bin/python
# -*- coding:utf-8 -*-
import threading

from flask import Flask, render_template

from appli_web.data.data_graph_making import graph_camembert_consomation_totale, graph_elec_consommation, \
    graph_gaz_consommation, graph_eau_consommation, graph_top10, graph_interactif

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.route('/')
def show_accueil():
    return render_template('home.html')

@app.route('/stats')
def show_test():
    graph_camembert_consomation_totale()
    return render_template('stats.html')

@app.route('/electricite')
def show_elec():
    graph_elec_consommation()
    return render_template('elec.html')

@app.route('/gaz')
def show_gaz():
    graph_gaz_consommation()
    return render_template('gaz.html')

@app.route('/eau')
def show_eau():
    graph_eau_consommation()
    return render_template('eau.html')

@app.route('/top10')
def show_top10():
    graph_top10()
    return render_template('top10.html')

@app.route('/analyse')
def show_analyse():
    graph_interactif()
    return render_template('analyse.html')

if __name__ == '__main__':
    app.run(debug=True)