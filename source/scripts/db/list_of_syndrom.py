# -*-coding:Utf-8 -*
from mongoObjects.Symptome import Symptome


def scrawl_file(name):
    Symptome.drop_collection()
    with open(name) as fich:
        ligne = fich.read()
        if ligne != "":
            Symptome(name=ligne).save()


def main():
    scrawl_file('data/list_of_symptome.txt')
if __name__ == "__main__":
    #main()
    Symptome.display()
