import imaplib
import email
import smtplib
from email.utils import parseaddr
import time

def send_mail(text_plain):
    server = smtplib.SMTP('smtp.gmail.com:25',587)
    server.starttls()
    server.ehlo()
    server.login("complaints.iiitv@gmail.com", "Pass123!@#")
    server.connect("smtp.gmail.com:465")
    server.sendmail("complaints.iiitv@gmail.com", "201651018@iiitv.ac.in", text_plain)
    server.quit()

def main():
    send_mail_mail("Vande Matram")


if __name__ == '__main__':
    main()