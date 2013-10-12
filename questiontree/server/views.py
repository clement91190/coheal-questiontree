from flask import render_template
from questiontree.server import app 
from questiontree.db import models


@app.route('/modify')
def modify():
    questions = models.Question.objects(q_type=models.Question.TYPE_SYMPTOME)
    print len(questions)
    return render_template(
        'modify.html',
        questions=questions)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/simu')
def simulate():
    return render_template('simulate.html')


@app.route('/findandmodify')
def findandmodify():
    question = models.Question.objects(q_id=models.Question.TYPE_SYMPTOME).first()
    return question.to_json()


@app.route('/test')
def test():
    return render_template('test.html')
