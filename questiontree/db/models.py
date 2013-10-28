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

    @staticmethod
    def path_length(id1, id2, temp=0):
        temp += 1
        if id1 == id2:
            return 0
        if temp < Graph.objects().count():
            list_of_length = [Graph.path_length(id, id2, temp) for id in Graph.objects(q_id=id1).first()]
            return 1 + min(list_of_length)
        else:
            #  saturation 
            return Graph.objects().count()
   
    def mean_path_length(self):
        """ generate the mean of the path length
        over the rest of the graph """
        s = 0
        tasks = zip(
            [g.q_id for g in Graph.objects()], 
            [False for q in Graph.objects()])
        temp = 0
        node_already_seen = set()
        new_nodes = set([self.q_id])
        sat = Graph.objects.count()
        while not all([b for id, b in tasks]) and temp < sat:
            new_nodes.difference(node_already_seen)
            s += temp * len(new_nodes)
            for n in new_nodes:
                tasks[n] = True
            l = list(new_nodes)
            node_already_seen.union(new_nodes)    
            new_nodes = set([])
            for n in l:
                new_nodes.union(set(Graph.objects(q_id=n).edges))
            
        self.mean_path_length = s * 1.0 / sat

    @staticmethod
    def gen_mean_paths(self):
        for n in Graph.objects():
            n.mean_path_length()


class TreeStructure(Document):
    q_id = IntField()
    children = ListField()
    # float numbers to determine logical movement inside the tree
    treshold = ListField() 
    
    @staticmethod
    def get_tree():
        """return the tree using JSON format"""
        pass
