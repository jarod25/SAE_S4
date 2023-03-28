#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint
import data.data_graph_making as graph

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/test')
def show_test():
    graph.graphique_barres_empilees()
    return render_template('consommation_par_annee_filiere.html')


if __name__ == '__main__':
    app.run()
