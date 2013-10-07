import traceback
import flask
from flask import jsonify
from questiontree.server import app

@app.route('/modify')
def modify():
    return "hello raph !"


