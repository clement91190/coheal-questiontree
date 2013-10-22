# -*-coding:Utf-8 -*
from mongoengine import Document, StringField, IntField, ListField,\
    register_connection


QUESTION_URI = 'mongodb://clement91190:rafiki@lafleur.mongohq.com:10078/app18535327'
QUESTION_ALIAS = 'question-tree-production'


print "connecting to question-tree database"
register_connection(QUESTION_ALIAS, 'question-tree-production', host=QUESTION_URI)


class Question(Document):
    """
    Generic Document for questions.
    """
    meta = {
        'db_alias': 'question-tree-production',
        'collection': 'question'}
    q_id = IntField()
    q_type = IntField()
    tags = ListField()
    symptome = StringField()
    question_text = StringField()
    answer_choices = ListField()

    TYPE_SYMPTOME = 2
    TYPE_GENERIQUE = 1


class Tags(Document):
    """
    class to store all the tags
    """
    meta = {
        'db_alias': 'question-tree-production',
        'collection': 'tags'}
    tag_id = IntField()
    text = StringField()
    translation = StringField()
    appearance = IntField()
    #describe the relation to the other tags (appearance of both)
    relation = ListField()  

