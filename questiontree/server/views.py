# -*-coding:Utf-8 -*
from flask import render_template, request
from questiontree.server import app 
from questiontree.db import models
import traceback
import json
import random


@app.route('/autocomplete_tags')
#TODO add to the tag page and delete
def autocomplete_tags():
    """ temporary page to test autocomplete """ 
    return render_template('autocomplet_tags.html')
        

@app.route('/tags')
def tags():
    """display an interface to see tags and ban some of them"""
    page = request.args.get('p')
    try:
        page = int(page)
    except:
        page = 0
    if page is None:
        page = 0
    #tags = models.Tag.objects(banned__ne=True)[page * 50:(page + 1) * 50]
    tags = models.Tag.objects().order_by('-id')
    return render_template('tags.html', tags=tags)


@app.route('/modify')
def modify():
    """ principal page to be able to modify the questions"""
    questions = models.Question.objects().order_by('valid', '-id')
    tags = models.Tag.objects()
    tags_dict = {t.id: t.text for t in tags}
    return render_template(
        'modify.html',
        questions=questions,
        enumerate=enumerate,
        tags=tags_dict)


@app.route('/modifyone')
def modifyone():
    """ access to one of the questions """
    try:
        id = request.args.get('id')
        tags = models.Tag.objects()
        tags_dict = {t.id: t.text for t in tags}
        question = models.Question.objects.get(id=id)
        return render_template(
            'modify.html',
            questions=[question],
            enumerate=enumerate,
            tags=tags_dict)
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


@app.route('/simulate')
def simulate():
    """ Page to simulate the questions """
    question = next_question()
    tags = []
    return render_template(
        'simulate.html',
        q=question,
        enumerate=enumerate,
        tags=tags)


@app.route('/delete_tag_from_db', methods=['POST'])
def delete_tag_from_db():
    """delete the tag from the database"""
    tag_id = request.form['tag_id']
    tag = models.Tag.objects(id=tag_id).first()
    tag.delete()
    return ""


@app.route('/findandmodify', methods=['POST'])
def findandmodify():
    """ modify the question """
    try: 
        id = request.form['id']
        qtext = request.form['qtext']
        question = models.Question.objects.get(id=id)
        question.question_text = qtext
        question.save()
        return template_modify_all_tags(question)
    except:
        print traceback.print_exc()
        return False


@app.route('/findandmodifysymp', methods=['POST'])
def findandmodifysymp():
    try: 
        id = request.form['id']
        text = request.form['symptometext']
        question = models.Question.objects.get(id=id)
        question.symptome = text
        question.save()
        return template_modify_all_tags(question)
    except:
        print traceback.print_exc()
        return False


@app.route('/addtag', methods=['POST'])
def addtag():
    try:
        id = request.form['id']
        tag_text = request.form['tag_text']
        tag = models.Tag.get_create(tag_text)
        question = models.Question.objects.get(id=id)
        question.tags_ids.append(tag.id)
        question.save()
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/deltag', methods=['POST'])
def del_tag():
    try:
        id = request.form['id']
        tag_id = request.form['tag_id']
        tag_id = int(tag_id)
        question = models.Question.objects.get(id=id)
        del(question.tags_ids[tag_id])
        question.save()
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/delete_answer_from_question', methods=['POST'])
def delete_answer_from_question():
    try:
        id = request.form['id']
        ans_id = request.form['ans_id']
        ans_id = int(ans_id)
        question = models.Question.objects.get(id=id)
        try:
            del(question.logic[question.answer_choices[ans_id]])
        except:
            pass
        del(question.answer_choices[ans_id])
        question.save()
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/delete_tag_inference_in_answer', methods=['POST'])
def delete_tag_inference_in_answer():
    try:
        id = request.form['id']
        ans_id = request.form['ans_id']
        tag_num = request.form['tag_num']
        ans_id = int(ans_id)
        tag_num = int(tag_num)
        question = models.Question.objects.get(id=id)
        del(question.logic[question.answer_choices[ans_id]][tag_num])
        question.save()
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/modify_answer_from_question', methods=['POST'])
def modify_answer_from_question():
    try:
        id = request.form['id']
        ans_id = request.form['ans_id']
        ans_text = request.form['ans_text']
        ans_id = int(ans_id)
        #TODO move this as a function in models.
        question = models.Question.objects.get(id=id)
        question.logic[ans_text] = question.logic[question.answer_choices[ans_id]]
        del(question.logic[question.answer_choices[ans_id]])
        question.answer_choices[ans_id] = ans_text
        question.save()
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False

 
@app.route('/add_tag_inference_in_answer', methods=['POST'])
def add_tag_inference_in_answer():
    try:
        id = request.form['id']
        ans_id = request.form['ans_id']
        ans_tag_text = request.form['ans_tag_text']
        positive = True
        if ans_tag_text[0] == '-':
            #this is an anti-tag
            ans_tag_text = ans_tag_text[1:]
            positive = False
        tag_id = models.Tag.get_create(ans_tag_text).id
        ans_id = int(ans_id)
        question = models.Question.objects.get(id=id)
        try:
            question.logic[question.answer_choices[ans_id]].append((positive, tag_id))
        except:
            question.logic[question.answer_choices[ans_id]] = []
            question.logic[question.answer_choices[ans_id]].append((positive, tag_id))
        question.save()
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/answer_simulation', methods=['POST'])
def answer_simulation():
    try:
        id = request.form['id']
        answer_choice = request.form['answer_choice']
       
        question = next_question()
        #TODO add something her to do useful stuff with answer
        #return json.dumps({"success": True})
        return template_simulate_question(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/validate_question', methods=['POST'])
def validate_question():
    try:
        id = request.form['id']
        question = models.Question.objects.get(id=id)
        question.valid = True
        question.save()
        #return json.dumps({"success": True})
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/unvalidate_question', methods=['POST'])
def unvalidate_question():
    try:
        id = request.form['id']
        question = models.Question.objects.get(id=id)
        question.valid = False
        question.save()
        #return json.dumps({"success": True})
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/add_answer', methods=['POST'])
def add_answer():
    try:
        id = request.form['id']
        ans_text = request.form['ans_text']
        question = models.Question.objects.get(id=id)
        question.answer_choices.append(ans_text)
        question.logic[ans_text] = []
        question.save()
        #return json.dumps({"success": True})
        return template_modify_all_tags(question)
    except:
        print "##fail##"
        print traceback.print_exc()
        return False


@app.route('/delquestion', methods=['POST'])
def delquestion():
    """ delete a question with the id given """
    try:
        id = request.form['id']
        models.Question.objects.get(id=id).delete()
        return ""
    except:
        print traceback.print_exc()


@app.route('/update_priority_question', methods=['POST'])
def update_priority_question():
    """ delete a question with the id given """
    try:
        id = request.form['id']
        priority = request.form['priority']
        priority = float(priority)
        question = models.Question.objects.get(id=id)
        question.priority = priority
        question.save()
        return template_modify_all_tags(question)
    except:
        print traceback.print_exc()


@app.route('/add_question', methods=['POST'])
def add_question():
    """ delete a question with the id given """
    try:
        question = models.Question()
        question.priority = 0
        question.symptome = "Symptome (optionnel)" 
        question.question_text = " Texte de la question a modifier"
        question.tags_ids = []
        question.answer_choices = []
        question.logic = {}
        question.save()

        print question.id
        return question.to_json()
    except:
        print traceback.print_exc()


@app.route('/test')
def test():
    question = models.Question.objects().first()
    tags = models.Tag.objects(id__in=question.tags_ids)
    response = {"question": json.loads(question.to_json()), "tags": json.loads(tags.to_json())}
    return json.dumps(response)
# return render_template('test.html')


@app.route('/search_tags')
def search_tags():
    """ return the first 5 tags starting with the key """
    try:
        key = request.args.get('key')
        print key
        list_of_tags = models.Tag.search_autocomplete(key)
        result = {"found": len(list_of_tags) != 0, "tags": list_of_tags}
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


def template_modify_all_tags(question):
    tags = models.Tag.objects()
    tags_dict = {t.id: t.text for t in tags}
    return template_modify(question, tags_dict) 
  

def template_modify(question, tags):
    return render_template(
        "modify_one_template.html", q=question,
        tags=tags, enumerate=enumerate)


def template_simulate_question(question):
    return render_template(
        "question_simulate_template.html", q=question,
        tags=tags, enumerate=enumerate)


def next_question():
    """ temporary function to get a random question """ 
    return random.choice(models.Question.objects(valid=True))


