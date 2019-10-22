import random
from datetime import datetime
from urllib.request import urlopen

def splitbytag(x):
    list_tags=x.split("#")
    print(list_tags)
    return list_tags

def create_picID(user_id):

    ra = round((random.random()*10000000000))
    req = urlopen('http://just-the-time.appspot.com/')

    time  = datetime.strptime(req.read().strip().decode('utf-8'), '%Y-%m-%d %H:%M:%S')
    stringtime=str(time.year)+str(time.month)+str(time.day)+str(time.hour)+str(time.minute)+str(time.second)+'_'+str(ra);
    return stringtime+str(user_id)

x="ada#adsa#sss#sda"
splitbytag(x)
for x in range(0,10):
    print(create_picID("abc"))

