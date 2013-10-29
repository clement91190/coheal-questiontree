# -*-coding:Utf-8 -*
import questiontree.db.models as models


def save_to_db(tags):
    for t, imp in tags.items():
        a, create = models.Tag.objects().get_or_create(text=t)
        if create:
            a.appearance = imp
        else:
            a.appearance += imp
        a.save()
        print "taking care of {}".format(t)


def main():
    tags = {}
    with open('data.txt', 'r') as fich:
        for l in fich:
            try:
                tags[l] += 1
            except:
                tags[l] = 0
    threshold = 3
    with open('data2.txt', 'w+') as fich:
        for w, i in tags.items():
            if i > threshold:
                fich.write(w)
            else:
                del(tags[w])
    print sorted(tags.items(), key=lambda (k, t): t)
    print " {} tags are still here".format(len(tags))
    save_to_db(tags)

if __name__ == "__main__":
    main()
