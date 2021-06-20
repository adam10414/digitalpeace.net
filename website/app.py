"""
This Flask app contains all of the routes necessary to run digitalpeace.net
"""

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

server = Flask(__name__, static_url_path='/static')
server.config['SECRET_KEY'] = 'my_secret'


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/austin')
def austin():
    return render_template('austin.html')


@server.route('/adam')
def adam():
    return render_template('adam.html')


@server.route('/submit')
def submit_post():
    return render_template('submit.html')


@server.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404