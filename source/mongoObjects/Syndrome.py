# -*-coding:Utf-8 -*

from mongoengine import IntField
from mongoengine import Document
from mongoengine import StringField


class Syndrome(Document):
    id = IntField()
    name = StringField()
    short_description = StringField()
    long_description = StringField()
    #scrawler_links = EmbeddedDocumentField()
    #user_links = EmbeddedDocumentField()
