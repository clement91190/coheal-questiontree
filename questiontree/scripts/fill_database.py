# petit script pour remplir la base de donnee de questions
import questiontree.db.models as models

with open('questiontree/data/list_of_symptome.txt') as fich:
    for symptome in fich:
        if symptome != "":
            q = models.Question(
                q_id=models.Question.objects().count(),
                q_type=2,
                tags=[symptome], symptome=symptome,
                question_text="Souffrez vous de {} ? ".format(symptome))
            q.save()
