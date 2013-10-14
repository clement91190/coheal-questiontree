from flask import render_template, request
from questiontree.server import app 
from questiontree.db import models
import traceback

@app.route('/modify')
def modify():
    questions = models.Question.objects(q_type=models.Question.TYPE_SYMPTOME)
    print len(questions)
    return render_template(
        'modify.html',
        questions=questions)


@app.route('/modifyone')
def modifyone():
    try:
        id = request.args.get('id')
        id = int(id)
        question = models.Question.objects(q_id=id).first()
        return render_template('modify_one.html', question=question)
    except:
        traceback.print_exc()
        return "not good" 


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/simu')
def simulate():
    return render_template('simulate.html')


@app.route('/findandmodify', methods=['POST'])
def findandmodify():
    try: 
        q_id =  request.form['q_id']
        qtext =  request.form['qtext']
        question = models.Question.objects(q_id=q_id).first()
        question.question_text = qtext
        question.save()
        return question.to_json()
    except:
        print traceback.print_exc()
        return False

@app.route('/test')
def test():
    return render_template('test.html')
