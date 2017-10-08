import imaplib
import email
import smtplib
from email.mime.application import MIMEApplication
from email.utils import parseaddr
import time
from os.path import basename
from os.path import isfile


def send_mail(to_id, subject, body, attach_path):
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
    if attach_path is not None and isfile(attach_path):
        with open(attach_path, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(attach_path)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attach_path)
        msg.attach(part)

    mailServer = smtplib.SMTP_SSL('smtp.gmail.com:465')

    mailServer.login(from_id, from_password)
    mailServer.sendmail(from_id, to_id, msg.as_string())
    mailServer.close()
    print("Mail sent")

# send_mail("201651018@iiitvadodara.ac.in", "Regarding compaints", "Serious issue in the attachment",None )