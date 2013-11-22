# petit script pour remplir la base de donnee de questions
import questiontree.db.models as models

with open('questiontree/scripts/crawler/wikiSpider/data.txt') as fich:
    for tag in fich:
        mytag, created = models.Tag.objects().get_or_create(text=tag)
        print mytag
        if mytag.appearance:
            mytag.appearance += 1 
        else:
            mytag.appearance = 1 
        mytag.save()

models.Tag.clean_data()


