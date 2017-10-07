import imaplib
import email
import smtplib
from email.utils import parseaddr
import time
import smtplib


def check_new_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('complaints.iiitv@gmail.com', 'Pass123!@#')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox") # connect to inbox.

    result, data = mail.uid('search', None, "UnSeen") # search and return uids instead

    if len(data[0].split()) != 0:

        for emailone in data[0].split():
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
            
             
            print(parseaddr(message.get('To'))[1])
            print(parseaddr(message.get('From'))[1])
            print(message.get('Subject'))
            print(text_plain)

while 1:
    check_new_mail()
    time.sleep(10)
