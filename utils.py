from datetime import datetime
from urllib.request import urlopen
from random import randint

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}


def create_picID(user_id):
    ra = randint(0, 10000000000)
    req = urlopen('http://just-the-time.appspot.com/')

    time = datetime.strptime(req.read().strip().decode('utf-8'), '%Y-%m-%d %H:%M:%S')
    stringtime = str(time.year) + str(time.month) + str(time.day) + str(time.hour) + str(time.minute) + str(
        time.second) + '_' + str(ra)
    return stringtime + str(user_id)


def split_by_tag(description):
    list_words = description.split(" ")
    list_tags = [word[1:] for word in list_words if word and word[0] == '#']
    return list_tags


if __name__ == '__main__':
    for x in range(0, 10):
        print(create_picID("abc"))

    x = "#attention please! this is a #test"
    y = "hello from #cs218 where #we are making a #project using #AWS"
    z = ""
    print(split_by_tag(x))
    print(split_by_tag(y))
    print(split_by_tag(z))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
