# -*-coding:Utf-8 -*

from mongoengine import Document
from mongoengine import ListField


class Diagnostic(Document):
    """ definition of the mongoDB object Diagnostic
    """
    results = ListField()  # list of the Syndroms and proba
    q_and_a = ListField()  # list of the question and answer that
# led to the diagnotic
    #patient_information = EmbeddedDocument()  #store info on patient
