import imaplib
import email
import smtplib
from email.utils import parseaddr
import time
import smtplib
import pymongo
from pymongo import MongoClient
import pprint

def check_new_mail(issue_no, posts, db):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('transport.iiitv@gmail.com', 'Pass123!@#')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox")  # connect to inbox.

    result, data = mail.uid('search', None, "UnSeen")  # search and return uids instead

    issue_array = []
    subject = []
    text = []
    if len(data[0].split()) != 0:
        for emailone in data[0].split():
            issue_no = issue_no + 1

            latest_email_uid = emailone
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = (data[0][1]).decode('utf-8')

            message = email.message_from_string(raw_email)
            text_plain = None
            text_html = None

            for part in message.walk():
                if part.get_content_type() == 'text/plain' and text_plain is None:
                    text_plain = part.get_payload()
                if part.get_content_type() == 'text/html' and text_html is None:
                    text_html = part.get_payload()

            to = parseaddr(message.get('To'))[1]
            From = parseaddr(message.get('From'))[1]
            subject.append(message.get('Subject'))
            text.append(text_plain)
            issue_array.append(issue_no)
            date = message.get("Date")
            
            post = {  # dictionary
                "to": to,
                "from": From,
                "subject": subject[-1],
                "text": text[-1],
                "date": date,
                "issue_no": issue_no,
                "status": "incomplete",
                "tag": "default.iiitv@gmail.com"
            }
            posts.insert_one(post).inserted_id



    return (issue_no, issue_array, subject, text, posts, db)

def fetch(issue_no,posts, db):
     print(posts.find_one({"issue_no" : 1}))

def update_tag(posts,db,issue_no,tag):
    print posts.find_one({"issue_no": issue_no})
    db.posts.update_one({
        'issue_no': issue_no
    }, {
        '$set': {
            'tag':tag
        }
    }, upsert=False)
    print posts.find_one({"issue_no": issue_no})
    return (posts,db)


def it( posts, db,mail):
    temp = mail
    for p in posts.find({"from":"diner.iiitv@gmail.com","status":"complete"}):
        mail[1]["com"] = mail[1]["com"] + 1
    for p in posts.find({"from":"diner.iiitv@gmail.com"}):
        mail[1]["op"]  = mail[1]["op"] + 1

    for p in posts.find({"from":"hec.iiitv@gmail.com","status":"complete"}):
        mail[2]["com"] = mail[2]["com"] + 1
    for p in posts.find({"from":"hec.iiitv@gmail.com"}):
        mail[2]["op"]  = mail[2]["op"] + 1

    for p in posts.find({"from":"cultural.iiitv@gmail.com","status":"complete"}):
        mail[3]["com"] = mail[3]["com"] + 1
    for p in posts.find({"from":"cultural.iiitv@gmail.com"}):
        mail[3]["op"]  = mail[3]["op"] + 1

    for p in posts.find({"from": "transport.iiitv@gmail.com", "status": "complete"}):
        mail[4]["com"] = mail[4]["com"] + 1
    for p in posts.find({"from": "transport.iiitv@gmail.com"}):
        mail[4]["op"] = mail[4]["op"] + 1

    for p in posts.find({"from":"academics.iiitv@gmail.com","status":"complete"}):
        mail[5]["com"] = mail[5]["com"] + 1
    for p in posts.find({"from":"academics.iiitv@gmail.com"}):
        mail[5]["op"]  = mail[5]["op"] + 1
    return(temp,mail)

def update( posts, db,issue_no,status):
    print(posts.find_one({"issue_no": 2}))
    db.posts.update_one({
        'issue_no': issue_no
    }, {
        '$set': {
            'status': status
        }
    }, upsert=False)
    print(posts.find_one({"issue_no": 2}))
    return (posts,db)


count = 0
client = MongoClient()
db = client.test_database
collection = db.test_collection
posts = db.posts
r = posts.delete_many({})
mail = {
    1:{ "comp":0 ,"op":0 },2:{ "comp":0 ,"op":0 },3:{ "comp":0 ,"op":0 },
    4:{ "comp":0 ,"op":0 },5:{ "comp":0 ,"op":0 }}
while 1:
    a, b, c, d, p, data = check_new_mail(count, posts, db)
 #   fetch(1,p,data)
    #update(p,data,2,"complete")
    #it(posts,db)
    update_tag(p,data,a,"diner.iiitv@gmail.com")
    count = a
    posts = p
    db = data

    time.sleep(10)