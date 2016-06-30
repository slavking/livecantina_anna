# coding: utf-8
from time import sleep
from livechanapi import *
import wikipedia
#import duckduckgo
import re
import os
import sys
import json
import requests
import random
#import wolframalpha
import urbandict
#from cleverbot import Cleverbot
import random
from datetime import datetime, timedelta
import config

import sqlite3
import shutil
import pickle
#from game import Game
#cb = Cleverbot()
#game = Game()

#def kc_quote(needle=None):
#    conn = sqlite3.connect('KC.db')
#    if needle:
#        cur = conn.execute('SELECT text FROM kcposts WHERE text LIKE ("%" || ? || "%") ORDER BY RANDOM() LIMIT 1', (needle,))
#        text = cur.fetchone()
#        if text:
#            return '\n'.join(line for line in text[0].splitlines() if not line.startswith('>>'))
#        else:
#            return

#    cur = conn.execute('SELECT text FROM kcposts ORDER BY RANDOM() LIMIT 1')
#    text = cur.fetchone()[0]
#    return '\n'.join(line for line in text.splitlines() if not line.startswith('>>'))


#def stats():
#    conn = sqlite3.connect('lb.sqlite')
#    cur = conn.execute('SELECT name,country,count(id) as c FROM posts GROUP BY ident ORDER BY c DESC LIMIT 20')
#    return '\n'.join('%s | %s | %s' % row for row in cur.fetchall())

#def online():
#    conn = sqlite3.connect('lb.sqlite')
#    cur = conn.execute('SELECT name,country FROM posts WHERE date>? GROUP BY ident', (datetime.now()-timedelta(minutes=3),))
#    return '\n'.join('%s | %s' % row for row in cur.fetchall())

#def countries():
#    conn = sqlite3.connect('lb.sqlite')
#    cur = conn.execute('SELECT country_name,count(id) as c FROM posts WHERE country_name!="" GROUP BY country_name ORDER BY c DESC LIMIT 20')
#    return '\n'.join('%s|%s' % row for row in cur.fetchall())

#def regions():
#    conn = sqlite3.connect('lb.sqlite')
#    cur = conn.execute('SELECT country,count(id) as c FROM posts WHERE country!="" GROUP BY country ORDER BY c DESC LIMIT 20')
#    return '\n'.join('%s|%s' % row for row in cur.fetchall())

def reddit(subreddit=None):
    if not subreddit:
        subreddit = 'manass'
    try:
        res = json.loads(requests.get('https://www.reddit.com/r/%s/top.json?sort=top&t=week&limit=100' % subreddit, headers={'User-Agent':'/r/your_user_name'}).text)['data']['children']
        post = random.choice(res)['data']
        text = post['title']
        if 'i.imgur.com' not in post['url'] and 'imgur.com' in post['url']:
            response = re.findall(r'(http://i.imgur.com/[\w\.]+)', requests.get(post['url']).text)
            if response:
                post['url'] = response[0]
        if "i.imgur.com" in post['url'] or post['url'].endswith('.jpg') or post['url'].endswith('.png'):
            response = requests.get(post['url'], stream=True)
            img = 'reddit%s' % os.path.splitext(post['url'])[1]
            with open(img, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            return (text, img)
        if post['url']:
            text += "\n%s" % post['url']
        if post.get('selftext'):
            text += "\n%s" % post['selftext']
        return (text, "anna" + str(random.randint(1,5)) + ".png")
    except Exception as e:
        print e
        return

def norris():
    res = requests.get('http://api.icndb.com/jokes/random')#, params={'firstName': '', 'lastName': ''})
    return res.json()['value']['joke']

refuse_message = "We're sorry. Please hang up and try again."

if (len(sys.argv) < 2):
    print "Usage: python anna.py [channel]"
    exit()
channel = sys.argv[1]
#wolfram = wolframalpha.Client(config.wolframAPI)

# globals
users = {}
replies = {
#    'russia':"Russia STRONG!",
#    'usa': "USA USA USA USA USA USA USA! Vote Trump! USA USA USA USA!",
    'weed': 'dude 420 lmao',
    'ayy': 'lmao',
#    'idiot': 'You want shit?',
}
annaposts = []
lastpost = datetime.now()

def process_chat(*args):
    img = "anna" + str(random.randint(6,8)) + ".png"
    try:
        ident = args[0]["identifier"]
        global users
        global lastpost
        global cb
        if ident in users:
            interval = (datetime.now() - users[ident]).total_seconds()
            #if interval < 7:
            #    return
        message = args[0]["body"]
        name = args[0]["name"]
        count = str(args[0]["count"])
        convo = args[0]["convo"]
#        country_name = args[0]["country_name"]
#        country = args[0]["country"]
        if "trip" in args[0]:
            trip = args[0]["trip"]
        else:
            trip = ""
        if trip == "!!n60sL82Wd2" and name == "anna":
            annaposts.append(count)
            return
        # default message
        out_message = ""

        if not message.strip().startswith('.'):
            with sqlite3.connect('lb.sqlite') as conn:
                conn.execute('INSERT INTO posts(id,ident,name,trip,convo,text,date) VALUES(?,?,?,?,?,?,?);',(count, ident, name, trip, convo, message, datetime.now()))
        

        for k, v in replies.items():
            if message.lower() == '.%s' % k:
                out_message = v

        #if (('to die' in message.lower() or 'death' in message.lower() or 'suicide' in message.lower()) and 'want' in message.lower()) or "kill me" in message.lower():
        #    out_message = random.choice(["Kill urself already.", "Just do it. Kill yourself.", "Suicide is the answer.", "Die"])

        # helpful
        
        if 'dat boi' in message.lower() or 'datboi' in message.lower():
            out_message = "O shit waddup"
        
#        t = re.compile('[wW]hat (is|are) (.+)\?').match(message)
#        if (t):
#            try:
#                res = wolfram.query(t.group(2))
#                #out_message = next(res.results).text
#                out_message = '\n'.join(z.text for z in res.pods[1:] if z)
#                #out_message = wikipedia.summary(t.group(1), sentences=1)
#            except Exception as e:
#                print res.__dict__
#                print out_message
#                out_message = ""
#                print "wolfram error",e

        # kc
#        t = re.compile('\.kc( (.+))?').match(message)
#        if (t):
#            res = kc_quote(t.group(1))
#            if res:
#                out_message = res


        # reddit
        t = re.compile('\.reddit( (.+))?').match(message)
        if (t):
            if t.group(1) and t.group(1).strip().replace('_','').isalpha() and not re.match('.*(4chan)',t.group(1)):
                res = reddit(t.group(1).strip())
            else:
                res = reddit()
            if res:
                out_message, img = res
        # urban
        t = re.compile('\.urban (.+)').match(message)
        if (t):
            res = ''
            for l in urbandict.define(t.group(1)):
                res += "def: %s\nexample: %s\n" % (l['def'].strip(), l['example'].strip())
            if res:
                out_message = res
        # play
#        t = re.compile('\.play( (.+))?').match(message)
#        if (t):
#            out_message, img = game.play(t.group(1), ident, name, country)
#            convo = "hangman"

        # wolfram
#        t = re.compile('\.wa (.+)').match(message)
#        if (t):
#            try:
#                res = wolfram.query(t.group(1))
#                out_message = next(res.results).text
#            except Exception as e:
#                out_message = refuse_message
#                #img = "anna" + str(random.randint(1,5)) + ".png"
#                img = "tila.jpg"
#                print e
         
        # wiki
        t = re.compile('\.wiki(pedia)? (.+)').match(message)
        if (t):
            try:
                out_message = wikipedia.summary(t.group(2), sentences=3)
            except wikipedia.DisambiguationError as e:
                out_message = str(e)
            except Exception as e:
                out_message = refuse_message
                #img = "anna" + str(random.randint(1,5)) + ".png"
                img = "tila.jpg"
                print e
     
        # google
#        t = re.compile('\.google( (.+))?').match(message)
#        if (t):
#            try:
#                r = duckduckgo.query(t.group(2))
#                for i in xrange(len(r.related) if len(r.related) < 4 else 3):
#                    result = r.related[i]
#                    out_message += '\n'+ result.text + '\n'
#                    out_message += '[i]' + result.url + ' [/i]\n'
#            except Exception as e:
#                out_message = refuse_message
#                #img = "anna" + str(random.randint(1,5)) + ".png"
#                img = "tila.jpg"
#                print e

        # random
        t = re.compile('\.random( (.+))?').match(message)
        if (t):
            try:
                if t.group(1) and t.group(2).isdigit():
                    out_message += str(random.randint(0, int(t.group(2))))
                else:
                    out_message += str(random.randint(0, 100))
                    if int(out_message)%10 == int(out_message)/10:
                        out_message += " (you got doubles :3)"
            except Exception as e:
                out_message = "That was ambiguous, Onii-chan"
                #img = "anna" + str(random.randint(1,5)) + ".png"
                img = "tila.jpg"
                print e
        # fortune
        t = re.compile('\.fortune( (.+))?').match(message)
        if (t):
            out_message = os.popen('fortune fortunes').read().strip()
            #out_message = os.popen('fortune').read().strip()
        
        # fortune-pl
        t = re.compile('\.fortunepl( (.+))?').match(message)
        if (t):
            out_message = os.popen('fortune pl').read().strip()
            
        # fortune-ru
        t = re.compile('\.fortuneru( (.+))?').match(message)
        if (t):
            out_message = os.popen('fortune ru').read().strip()
            
        # fortune-fr
        t = re.compile('\.fortunefr( (.+))?').match(message)
        if (t):
            out_message = os.popen('fortune fr').read().strip()
            
        # riddle
        t = re.compile('\.riddle( (.+))?').match(message)
        if (t):
            out_message = os.popen('fortune riddles').read().strip()
        # stats
        t = re.compile('\.stats( (.+))?').match(message)
        if (t):
            out_message = stats()
        # scores
#        t = re.compile('\.scores( (.+))?').match(message)
#        if (t):
#            out_message = game.stats()
        # online
#        t = re.compile('\.online( (.+))?').match(message)
#        if (t):
#            out_message = online()
        # countries
#        t = re.compile('\.countries( (.+))?').match(message)
#        if (t):
#            out_message = countries()
        # regions
#        t = re.compile('\.regions( (.+))?').match(message)
#        if (t):
#            out_message = regions()
        # joke
        t = re.compile('\.joke( (.+))?').match(message)
        if (t):
            out_message = norris()#random.choice(open('jokes.txt').read().split('\n-')).strip()
        # meme
#        t = re.compile('\.meme( (.+))?').match(message)
#        if (t):
#            out_message = " "
#            img = 'memes/'+random.choice(os.listdir('memes'))
        # hi
        t = re.compile('\.hi( (.+))?').match(message)
        if (t):
            out_message = "%s, %s!" % (random.choice(['Hi', 'Hello', 'Privet', 'Hola', 'Bonjour', 'Hallo']), name)
        # help
        t = re.compile('\.help( (.+))?').match(message)
        if (t):
            out_message = "commands are .hi .random .joke .fortune .fortuneru .fortunefr .fortunepl .google .urban .wa .wiki .riddle .reddit"
            out_message += '\nor "Anna ...?" or "What is/are ...?"'
        # porn
#        t = re.compile('\.porn( (.+))?').match(message)
#        if (t):
#            out_message = random.choice([
#                'You are wankaholic',
#                'You are addicted to masturbating',
#                'You are addicted to pornography',
#                'Hi wanka',
#                ])
#            img = 'wanka.jpg'
#            img = 'porn/'+random.choice(os.listdir('porn'))
#            convo = 'General'

        ## add
        #t = re.compile('\.add (\w+) (.+)').match(message)
        #if (t):
        #    #print t.groups(1)[0], t.groups(1)[1]
        #    replies[t.groups(1)[0]] = t.groups(1)[1]


        if (message.splitlines() and message.splitlines()[0].lstrip('>') in annaposts) or (message.lower().startswith('anna') and message.endswith('?')):
            try:
                if message.lower().startswith('anna'):
                    message = message[4:].strip()
                out_message = cb.ask(u'\n'.join(line for line in message.splitlines() if not line.startswith('>')))
            except Exception as e:
                out_message = refuse_message
                #img = "anna" + str(random.randint(1,5)) + ".png"
                img = "tila.jpg"
                print e
#                cb = Cleverbot()

        if count[-1]==count[-2]:
            out_message = "checked"
            img = "dubs" + str(random.randint(1,25)) + ".jpg"

		###this checks trips, quads, quints and septs
		###>you need not dubs folder but files dubs1.jpg - dubs5.jpg right in anna folder
		#if count[-1]==count[-2]==count[-3] or count[-1]==count[-2]==count[-3]==count[-4] or count[-1]==count[-2]==count[-3]==count[-4]==count[-5] or count[-1]==count[-2]==count[-3]==count[-4]==count[-5]==count[-6]:
		# out_message = "CHECKED"
		# img = "dubs" + str(random.randint(1,5)) + ".jpg"

        #if 'anna' in message.lower():
        #    out_message = "you said my name, Onii-chan?"
        #if 'kcmod' in message.lower():
        #    out_message = "mods are cucks"

#        if not out_message and random.randint(0,45) == 5 and (datetime.now() - lastpost).total_seconds() > 30:
#            print (datetime.now() - lastpost).total_seconds()
#            out_message = kc_quote()
#            count = 0

        if out_message != "":
            users[ident] = datetime.now()
            lastpost = datetime.now()
            if (count):
                out_message = ">>"+count+"\n"+out_message#.encode('ascii', 'ignore')
            post_chat(out_message, channel,
                    name="anna", trip=config.annaTrip,
                    convo=convo, file=img)
    except Exception as e:
        #print type(e), e
        #raise
        print e

login(callback=process_chat)
join_chat(channel)

while 1:
    sleep(10)