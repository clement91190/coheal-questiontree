# petit script pour remplir la base de donnee de questions
import questiontree.db.models as models

#with open('questiontree/data/list_of_symptome.txt') as fich:
#    for symptome in fich:

for q in models.Question.objects(q_id__gt=51):
    symptome = q.symptome
    q.question_text = "Vous arrive-t-il de " + symptome +" ?"
    q.save()
