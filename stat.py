import imaplib
import email
import smtplib
from email.utils import parseaddr
import time
import smtplib
import os
import sys

from pymongo import MongoClient


def check_new_mail(issue_no, posts, db):
    attach_list ={  }
    subject_re = []
    detach_dir = '.'
    if 'attachments' not in os.listdir(detach_dir):
        os.mkdir('attachments')
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('transport.iiitv@gmail.com', 'Pass123!@#')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox")  # connect to inbox.

    result, data = mail.uid('search', None, "UnSeen")  # search and return uids instead
    issue_array = []
    subject = []
    text = []
    ret_data = None
    if len(data[0].split()) != 0:
        ret_data = data[0].split()
        for emailone in data[0].split():
            print ("sd")
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

                fileName = part.get_filename()

            filePath = None

            if bool(fileName):
                filePath = os.path.join(detach_dir, 'attachments', fileName)
                if not os.path.isfile(filePath):

                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()


            to = parseaddr(message.get('To'))[1]
            From = parseaddr(message.get('From'))[1]
            sub = message.get('Subject')
            text_case = text_plain
            # issue_array.append(issue_no)
            if From.split('@')[1] == 'iiitvadodara.ac.in' or From.split('@')[1] == 'gmail.com':
                if sub[0:3] == 'Re:':
                    subject_re.append({'issue_no': int( sub.split()[1][1:]), 'sub': sub, 'body': text_case})
                else:
                    print (issue_no)
                    issue_no = issue_no + 1
                    subject.append(sub)
                    text.append(text_case)
                    issue_array.append(issue_no)
                    attach_list[issue_no] = filePath
                    print(attach_list)
                    date = message.get("Date")
                    post = {  # dictionary
                        "to": to,
                        "from": From,
                        "subject": subject[-1],
                        "text": text[-1],
                        "date": date,
                        "issue_no": issue_no,
                        "status": "incomplete",
                        "tag": "academics.iiitv@gmail.com"
                    }
                    posts.insert_one(post).inserted_id
                    print (post)
    print ("done checking")
    return (issue_no, issue_array, subject,  text, ret_data, mail, subject_re, attach_list, posts, db)


mail_dict = {
    1:{ "comp":0 ,"op":0 },2:{ "comp":0 ,"op":0 },3:{ "comp":0 ,"op":0 },
    4:{ "comp":0 ,"op":0 },5:{ "comp":0 ,"op":0 }}

def it( posts,mail_dict):


    for p in posts.find({"tag":"diner.iiitv@gmail.com","status":"complete"}):
        mail_dict[1]["comp"] = mail_dict[1]["comp"] + 1


    for p in posts.find({"tag":"diner.iiitv@gmail.com"}):
        mail_dict[1]["op"]  = mail_dict[1]["op"] + 1


    for p in posts.find({"tag":"hec.iiitv@gmail.com","status":"complete"}):
        mail_dict[2]["comp"] = mail_dict[2]["comp"] + 1

    for p in posts.find({"tag":"hec.iiitv@gmail.com"}):
        mail_dict[2]["op"]  = mail_dict[2]["op"] + 1


    for p in posts.find({"tag":"cultural.iiitv@gmail.com","status":"complete"}):
        mail_dict[3]["comp"] = mail_dict[3]["comp"] + 1
    for p in posts.find({"tag":"cultural.iiitv@gmail.com"}):
        mail_dict[3]["op"]  = mail_dict[3]["op"] + 1

    for p in posts.find({"tag": "transport.iiitv@gmail.com", "status": "complete"}):
        mail_dict[4]["comp"] = mail_dict[4]["comp"] + 1
    for p in posts.find({"tag": "transport.iiitv@gmail.com"}):
        mail_dict[4]["op"] = mail_dict[4]["op"] + 1

    for p in posts.find({"tag":"academics.iiitv@gmail.com","status":"complete"}):
        mail_dict[5]["comp"] = mail_dict[5]["comp"] + 1
    for p in posts.find({"tag":"academics.iiitv@gmail.com"}):
        mail_dict[5]["op"]  = mail_dict[5]["op"] + 1
    print (mail_dict)
    return mail_dict


def get_monthly_stats(mail_dict):

    x = mail_dict
    completed = []
    for i in range(5):
        completed.append(x[i+1]["comp"])
    opened = []
    for i in range(5):
        opened.append(x[i+1]["op"])
    incompleted = []
    #for i in range(5):
         #incompleted.append(opened[i+1] - completed[i+1])

    clear_dict()

    print(completed)
    print(opened)
    print(incompleted)

    return (completed, incompleted, opened)

def clear_dict():
    mail_dict.clear()


client = MongoClient()
db = client.test_database
collection = db.test_collection
posts = db.posts




a,b,c,d,e,f,g,h,posts,db = check_new_mail(0,posts,db)
mail_dict = it(posts, mail_dict)
get_monthly_stats(mail_dict)
