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

    @staticmethod
    def get_all_symptome():
        """ return a list of all symptome in the questions"""
        return [q.symptome for q in Question.objects(q_type=2)]


class Tag(Document):
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

    @staticmethod
    def clean_data():
        for i in Tag.objects(appearance__lt=2):
            print "delete {} ".format(i)
            i.delete()


class Graph(Document):
    """ Graph is a collection of Question with a Node/edges structure """
    q_id = IntField() 
    edges = ListField()
    weight = ListField()

    def get_question(self):
        """ return the question corresponding to q_id"""
        return Question.objects(q_id=self.q_id).first()

    def follow_edge(self, ind=1):
        """ follow the edge and return the node """
        node = Graph.objects(q_id=self.edges[ind])
        return node


class TreeStructure(Document):
    q_id = IntField()
    children = ListField()
    # float numbers to determine logical movement inside the tree
    treshold = ListField() 
    
    @staticmethod
    def get_tree():
        """return the tree using JSON format"""
        pass
