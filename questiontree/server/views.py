# -*-coding:Utf-8 -*
from flask import render_template, request
from questiontree.server import app 
from questiontree.db import models
import traceback
import json


@app.route('/autocomplete_tags')
#TODO add to the tag page and delete
def autocomplete_tags():
    """ temporary page to test autocomplete """ 
    return render_template('autocomplet_tags.html')
        

@app.route('/tags')
def tags():
    """display an interface to see tags and ban some of them"""
    page = request.args.get('p')
    page = int(page)
    if page is None:
        page = 0
    try:
        tags = models.Tag.objects(banned__ne=True)[page * 50:(page + 1) * 50]
    except:
        page = 0
        tags = models.Tag.objects(banned__ne=True)[page * 50:(page + 1) * 50]
    ban_tags = models.Tag.objects(banned=True)
    return render_template('tags.html', tags=tags, ban_tags=ban_tags)


@app.route('/modify')
def modify():
    """ principal page to be able to modify the questions"""
    questions = models.Question.objects(q_type=models.Question.TYPE_SYMPTOME).order_by('q_id')
    return render_template(
        'modify.html',
        questions=questions,
        enumerate=enumerate)


@app.route('/modifyone')
#TODO see if it is useful to keep ...
def modifyone():
    """ access to one of the questions """
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
    """ Help Page, empty now ... """
#TODO Complete for people using the interface
    return render_template('help.html')


@app.route('/question-generique')
#TODO Clean this  ?
def questiongeneriques():
    try:
        questions = models.Question.objects(q_type=models.Question.TYPE_GENERIQUE)
        return render_template('question_gen.html', questions=questions)
    except:
        return "not good"


@app.route('/simu')
def simulate():
    """ Page to simulate the questions """
    return render_template('simulate.html')


@app.route('/ban_tag', methods=['POST'])
def ban_tag():
    """ ban the corresponding tag ( change it's status in the database) """
    tag_id = request.form['tag_id']
    tag = models.Tag.objects(tag_id=tag_id).first()
    tag.banned = True
    tag.save()
    return "ok"


@app.route('/findandmodify', methods=['POST'])
def findandmodify():
    """ modify the question """
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
        tag = models.Tag.get_create(tag_text)
        question = models.Question.objects(q_id=q_id).first()
        question.tags_ids.append(tag.id)
        question.save()
        response = {"question": question.to_json(), "tags": models.Tag.objects(id__in=question.tags_ids)}
        return json.dumps(response)
    except:
        print traceback.print_exc()
        return False


@app.route('/deltag', methods=['POST'])
def del_tag():
    #TODO Change the way we access tags...
    try:
        q_id = request.form['q_id']
        tag_id = request.form['tag_id']
        tag_id = int(tag_id)
        q_id = int(q_id)
        question = models.Question.objects(q_id=q_id).first()
        del(question.tags_ids[tag_id])
        question.save()
        return question.to_json()
    except:
        print traceback.print_exc()
        print q_id
        print tag_id
        return False


@app.route('/delquestion', methods=['POST'])
def delquestion():
    """ delete a question with the id given """
    try:
        q_id = request.form['q_id']
        models.Question.objects(q_id=q_id).first().delete()
        return json.dumps({'success': True})
    except:
        print traceback.print_exc()
    

@app.route('/test')
def test():
    question = models.Question.objects().first()
    tags = models.Tag.objects(id__in=question.tags_ids)
    response = {"question": json.loads(question.to_json()), "tags": tags.to_json()}
    return response
# return render_template('test.html')


@app.route('/search_tags')
def search_tags():
    """ return the first 5 tags starting with the key """
    try:
        key = request.args.get('key')
        print key
        list_of_tags = models.Tag.search_autocomplete(key)
        result = {"found": len(list_of_tags) == 0, "tags": list_of_tags}
        return json.dumps(result)
    except:
        traceback.print_exc()
        return "coucou"
   

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
