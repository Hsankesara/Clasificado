import imaplib
import email
import smtplib
from email.utils import parseaddr
import time



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

            to = parseaddr(message.get('To'))[1]
            From = parseaddr(message.get('From'))[1]
            subject = (message.get('Subject'))

            
            
            #Add the code for fetching tag frommm watson here
            send_mail("ADD THE EMAIL ACCORDING TO TAG", subject,  text_plain)




def send_mail(to_id, subject, body):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    from_id = 'complaints.iiitv@gmail.com'
    from_password = 'Pass123!@#'

    msg = MIMEMultipart()
    msg['From'] = from_id
    msg['To'] = to_id
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    mailServer = smtplib.SMTP_SSL('smtp.gmail.com:465')

    mailServer.login(from_id, from_password)
    mailServer.sendmail(from_id, to_id, msg.as_string())
    mailServer.close()

while 1:
    check_new_mail()




