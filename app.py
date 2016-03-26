from flask import Flask, render_template, request,redirect
import os
from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
import json
import psycopg2
import urlparse
from challenge import Challenge

app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
fp = os.path.join(SITE_ROOT, 'config.json')
app = Flask(__name__)
global token
token = None
with open(fp) as cred:
    creds = json.load(cred)

app.config['GITHUB_CLIENT_ID'] = creds['id']
app.config['GITHUB_CLIENT_SECRET'] = creds['secret']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

github = GitHub(app)
db = SQLAlchemy(app)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return github.authorize()

@app.route('/callback')
@github.authorized_handler
def authorized(oauth_token):
    global token
    token = oauth_token
    data = github.get('user')
    data['token'] = token
    return render_template('profile.html', data=data)

@app.route('/challenges')
def challenges():
    return jsonify(Challenge.query.all())

@github.access_token_getter
def token_getter():
    return token

if __name__ == "__main__":
    app.debug=True
    app.run()
