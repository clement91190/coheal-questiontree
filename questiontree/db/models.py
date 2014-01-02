# -*-coding:Utf-8 -*
from mongoengine import Document, StringField, IntField, ListField,\
    register_connection, BooleanField, DictField, FloatField, ObjectIdField
import time

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
    tags_ids = ListField()
    symptome = StringField()
    question_text = StringField()
    answer_choices = ListField()
    logic = DictField()  # Dictionary to link an answer_choice to a list of a tuple (bool, ObjectId of Tag)
    priority = FloatField()
    valid = BooleanField()  # if True -> used in simulation

    TYPE_SYMPTOME = 2
    TYPE_GENERIQUE = 1

    @staticmethod
    def get_all_symptome():
        """ return a list of all symptome in the questions"""
        return [q.symptome for q in Question.objects(q_type=2)]

    @staticmethod
    def get_best_question(answer_session):
        #print map(lambda x: x.fitness(answer_session), Question.objects(valid=True))
        q = min(Question.objects(valid=True), key=lambda x: x.fitness(answer_session))
        if q.fitness(answer_session) == 100:
            return None
        else:
            return q

    def fitness(self, answer_session):
        """ function describing how good is the question knowing the items in
        inference_list"""
        ids_of_question_already_answered = [a[0] for a in answer_session.answers]
        print ids_of_question_already_answered
        if str(self.id) in ids_of_question_already_answered or self.priority is None:
            return 100
        return 1 - self.priority


class Tag(Document):
    """
    class to store all the tags
    """
    meta = {
        'db_alias': 'question-tree-production',
        'collection': 'tags'}
    text = StringField()
    translation = StringField()
    banned = BooleanField()

    @staticmethod
    def clean_data():
        """ delete Tags if they apppear twice """
        for t in Tag.objects():
            l = Tag.objects(text=t.text)
            if len(l) > 1:
                l[1].delete()
                         
    @staticmethod
    def search_autocomplete(key):
        """query for the autocompletion """
        return [t.text for t in Tag.objects(text__istartswith=key,banned__ne=True)][:5]

    @staticmethod
    def get_create(key):
        try:
            res, created = Tag.objects.get_or_create(text=key)
        except:
            print "DATABASE NOT CLEAN MULTIPLE OBJECTS"
            created = False
        if created:
            res.save()
        return res


class AnswerSession(Document):
    """ store all the question and answer off a User """
    meta = {
        'db_alias': 'question-tree-production',
        'collection': 'answer_session'}
    user_id = ObjectIdField()
    answers = ListField()  # list of tuple (Question Id, answer, timestamp)
    tags = ListField()  # List of ( bool,  Id of the tag) implied by the answers (or Patient Profile)

    def get_answered_questions(self):
        """ return the list of ids of questions already answered"""
        return [a[0] for a in self.answers] 

    def add_answer(self, question_id, answer_num):
        q = Question.objects.get(id=question_id)
        tags_to_add = q.logic[q.answer_choices[answer_num]]
        tags = set([tuple(t) for t in self.tags])
        tags_to_add = set([tuple(t) for t in q.logic[q.answer_choices[answer_num]]])
        for t in set(tags_to_add).difference(tags):
            self.tags.append(t)
        self.answers.append((question_id, answer_num, int(time.time())))
        self.save()
    
    def get_tags_anti_tags(self):
        return [(b, Tag.objects.get(id=id).text) for b, id in self.tags]


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
