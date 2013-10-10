import traceback
from flask import jsonify, render_template
from questiontree.server import app

@app.route('/modify')
def modify():
    return render_template('template.html')


