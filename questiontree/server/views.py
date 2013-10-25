from flask import render_template, request
from questiontree.server import app 
from questiontree.db import models
import traceback
import json

@app.route('/modify')
def modify():
    questions = models.Question.objects(q_type=models.Question.TYPE_SYMPTOME).order_by('q_id')
    print len(questions)
    return render_template(
        'modify.html',
        questions=questions,
        enumerate=enumerate)


@app.route('/modifyone')
def modifyone():
    try:
        id = request.args.get('id')
        id = int(id)
        question = models.Question.objects(q_id=id).first()
        return render_template(
            'modify_one.html',
            question=question,
            enumerate=enumerate)
    except:
        traceback.print_exc()
        return "not good" 


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/question-generique')
def questiongeneriques():
    try:
        questions = models.Question.objects(q_type=models.Question.TYPE_GENERIQUE)
        return render_template('question_gen.html', questions=questions)
    except:
        return "not good"


@app.route('/simu')
def simulate():
    return render_template('simulate.html')


@app.route('/findandmodify', methods=['POST'])
def findandmodify():
    try: 
        q_id = request.form['q_id']
        qtext = request.form['qtext']
        question = models.Question.objects(q_id=q_id).first()
        question.question_text = qtext
        question.save()
        return question.to_json()
    except:
        print traceback.print_exc()
        return False


@app.route('/findandmodifysymp', methods=['POST'])
def findandmodifysymp():
    try: 
        q_id = request.form['q_id']
        text = request.form['symptometext']
        question = models.Question.objects(q_id=q_id).first()
        question.symptome = text
        question.save()
        return question.to_json()
    except:
        print traceback.print_exc()
        return False


@app.route('/addtag', methods=['POST'])
def addtag():
    try:
        q_id = request.form['q_id']
        tag_text = request.form['tag_text']
        question = models.Question.objects(q_id=q_id).first()
        question.tags.append(tag_text)
        question.save()
        return question.to_json()
    except:
        print traceback.print_exc()
        return False


@app.route('/deltag', methods=['POST'])
def del_tag():
    try:
        q_id = request.form['q_id']
        tag_id = request.form['tag_id']
        tag_id = int(tag_id)
        q_id = int(q_id)
        question = models.Question.objects(q_id=q_id).first()
        del(question.tags[tag_id])
        question.save()
        return question.to_json()
    except:
        print traceback.print_exc()
        print q_id
        print tag_id
        return False


@app.route('/delquestion', methods=['POST'])
def delquestion():
    try:
        q_id = request.form['q_id']
        models.Question.objects(q_id=q_id).first().delete()
        return json.dumps({'success': True})
    except:
        print traceback.print_exc()
    

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/get_question')
def get_question():
    try:
        id = request.args.get('id')
        id = int(id)
        question = models.Question.objects(q_id=id).first()
        return question.to_json() 
    except:
        traceback.print_exc()
        return False 
