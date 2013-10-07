from flask import Flask
from flask.ext.basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'rafiki'
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True

import views
