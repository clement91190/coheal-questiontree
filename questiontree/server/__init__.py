from flask import Flask
from flask.ext.basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'rafiki'
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True
app.secret_key = '\x85\xe7\x1e\xb3\xa8;\n\xd1\xf2\t\xb1\x14"%?\x03}dt\x16>K\x88\x1a'
import views
