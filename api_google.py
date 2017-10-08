import imaplib
import email
import smtplib
from email.utils import parseaddr
import time
import smtplib
import os
import sys


def check_new_mail(issue_no, posts, db):
    attach_list ={  }
    subject_re = []
    detach_dir = '.'
    if 'attachments' not in os.listdir(detach_dir):
        os.mkdir('attachments')
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('complaints.iiitv@gmail.com', 'Pass123!@#')
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
            print "sd"
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
                        "tag": "default.iiitv@gmail.com"
                    }
                    posts.insert_one(post).inserted_id
                    print post
    print "done checking"
    return (issue_no, issue_array, subject,  text, ret_data, mail, subject_re, attach_list, posts, db)
