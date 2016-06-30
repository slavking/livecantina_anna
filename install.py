#!/usr/bin/python
import os
import sqlite3

os.system('sudo pip install -r requirements.txt')

dirs = ('memes', 'reddit', 'porn')

for dirname in dirs:
    if not os.path.exists(dirname):
        os.mkdir(dirname)

conn = sqlite3.connect('KC.db')
conn.execute(open('KC.db.scheme').read())

conn = sqlite3.connect('lb.sqlite')
conn.execute(open('lb.sqlite.scheme').read())

print 'put some files into dirs: ', dirs
print 'add some records to sqlite database KC.db'

