import imaplib
import email
import smtplib
from email.utils import parseaddr
import time

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
    print "Mail sent"