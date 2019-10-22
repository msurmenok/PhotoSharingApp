{\rtf1\ansi\ansicpg1252\cocoartf2509
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import random\
from datetime import datetime\
from urllib.request import urlopen\
\
def create_picID(user_id):\
\
    ra = round((random.random()*10000000000))\
    req = urlopen('http://just-the-time.appspot.com/')\
\
    time  = datetime.strptime(req.read().strip().decode('utf-8'), '%Y-%m-%d %H:%M:%S')\
    stringtime=str(time.year)+str(time.month)+str(time.day)+str(time.hour)+str(time.minute)+str(time.second)+'_'+str(ra);\
    return stringtime+str(user_id)\
\
\
for x in range(0,10):\
    print(create_picID("abc"))\
}