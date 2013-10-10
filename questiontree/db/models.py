# -*-coding:Utf-8 -*

from mongoengine import Document, StringField, IntField, ListField,\
    register_connection
import urllib2


QUESTION_URI = 'mongodb://clement91190:rafiki@lafleur.mongohq.com:10078/app18535327'
QUESTION_ALIAS = 'question-tree-production'


print "connecting to question-tree database"
register_connection(QUESTION_ALIAS, 'question-tree-production', host=QUESTION_URI)



class Question(Document):
    """
    Generic Document for questions.
    """
    meta = {
            'db_alias':'question-tree-production',
            'collection': 'question'}
    q_id = IntField()
    q_type = IntField()
    tags = ListField()
    symptome = StringField()
    question_text = StringField()


