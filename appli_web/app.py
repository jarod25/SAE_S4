#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from appli_web.data.data_graph_making import graph, graph_elec_consommation, graph_gaz_consommation, graph_eau_consommation, graph_top10

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.route('/')
def show_accueil():
    return render_template('home.html')

@app.route('/test')
def show_test():
    graph()
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run()
