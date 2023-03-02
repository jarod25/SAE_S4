#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint
import api_requests

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('index.html')


@app.route('/first_request')
def first_request():
    req = api_requests.first_request()
    return render_template('first_request.html', req=req)


@app.route('/second_request')
def second_request():
    req = api_requests.second_request()
    req = req['records'][0]
    return render_template('second_request.html', req=req)


if __name__ == '__main__':
    app.run()
