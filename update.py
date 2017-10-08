import imaplib
import email
import smtplib
from email.utils import parseaddr
import time
import smtplib
import pymongo
from pymongo import MongoClient

def update( pots, db,issue_no,status):
    db.posts.update_one({
        'issue_no': issue_no
    }, {
        '$set': {
            'status': status
        }
    }, upsert=False)
    return (pots,db)

def update_tag(posts,db,issue_no,tag):
    db.posts.update_one({
        'issue_no': issue_no
    }, {
        '$set': {
            'tag':tag
        }
    }, upsert=False)
    return (posts, db)





def fetch(issue_no,pots, db):
    return posts.find_one({"issue_no":issue_no})

client = MongoClient()
db = client.test_database
collection = db.test_collection
posts = db.posts
tag = "transport.iiitv@gmail.com"
post = {  # dictionary
                    "to": "a",
                    "from": "b",
                    "subject": "c",
                    "text": "d",
                    "date": "asd",
                    "issue_no": 1,
                    "status": "incomplete",
                    "tag": tag
                }
posts.insert_one(post).inserted_id
for p in posts.find_one():
    print(p)
fetch(1,posts,db)
issue_no = 1
while 1:
    p,data = update( posts, db,issue_no,"completed")
    #count = a
    posts = p
    db = data
    #staus = s
    time.sleep(10)