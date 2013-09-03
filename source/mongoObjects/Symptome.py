# -*-coding:Utf-8 -*

from mongoengine import IntField
from mongoengine import Document
from mongoengine import StringField
import mongoObjects.DbConnection


class Symptome(Document):
    """ definition of the mongoDB object Symptome
    """
    id = IntField()
    name = StringField()
    short_description = StringField()
    long_description = StringField()

    @staticmethod
    def display():
        for s in Symptome.objects():
            print s.name
