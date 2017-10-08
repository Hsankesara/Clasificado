import imaplib
import email
import smtplib
from email.utils import parseaddr
import time
import smtplib
import pymongo
import pprint
from pymongo import MongoClient


def check_new_mail(issue_no):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('transport.iiitv@gmail.com', 'Pass123!@#')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox")  # connect to inbox.

    result, data = mail.uid('search', None, "UnSeen")  # search and return uids instead

    client = MongoClient()
    db = client.test_database
    collection = db.test_collection
    posts = db.posts
    pos1   = db.pos1

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
            subject = message.get('Subject')
            text = text_plain
            date = message.get("Date")
            post = {  # dictionary
                "to": to,
                "from": From,
                "subject": subject,
                "text": text,
                "date": date,
                "issue_no": issue_no,
                "status": "incomplete",
                "tag": "default.iiitv@gmail.com"
            }

            print("monal chutiya hai")

            posts.insert(post)


        for p in posts.find({"subject":"can"}):
            print(p)
    return issue_no


count = 0
while 1:
    x = check_new_mail(count)
    count = x
    time.sleep(10)