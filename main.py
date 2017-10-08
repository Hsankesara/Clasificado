import watson_access as watson
import api_google as api
import sent_mail
import time
from pymongo import MongoClient
import pprint
import db_func
import datetime

def get_tags(subject, text, is_student):
    subject_tag = None
    if subject is not None:
        subject_tag = watson.get_classified_tag(subject, is_student)
    body_tags = None
    if text is not None:
        body_tags = []
        for para in text:
            if para is not None and para != '': 
                body = para.split('.')
                for part in body:
                    new_tag = watson.get_classified_tag(part, is_student)
                    if new_tag != 'Spam':
                        body_tags.append(new_tag)
    print 'subject_tag = ', subject_tag,'body_tag = ', body_tags
    return (subject_tag, body_tags)

def main():
    '''
    MESS = 'diner.iiitv@gmail.com'
    ACAD = 'academics.iiitv@gmail.com'
    SPORTS = 'cultural.iiitv@gmail.com'
    CULTURAL = 'cultural.iiitv@gmail.com'
    HEC = 'hec.iiitv@gmail.com'
    BUS = 'bus.iiitv@gmail.com'
    '''
    client = MongoClient()
    db = client.test_database
    collection = db.test_collection
    posts = db.posts
    issue_number = 0
    s = '\r\n'
    while 1:
        issue_number, issue_array, subject, text, uid, mail, subject_re, attach_list, posts, db = api.check_new_mail(issue_number, posts, db)
        # Test get_tags
        #  subject = "regarding bus schedule"
        # text = """Sir, Our bus schedule is not according to our classes.\r\nSo many times we are facing difficulties to attend class.\r\nKindly cancel all the classes.\r\nwith regards\r\nHeet Sankesara"""
        for i in range(len(issue_array)):
            if text[i] is not None:
                text[i] = text[i].split("\r\n")
            else:
                text[i] = None
            subject_tag, body_tags = get_tags(subject[i], text[i], True)
            # final_tag = get_final_tag(subject_tag, body_tags)
            # edit final tag
            final_tag = subject_tag + '@gmail.com'
            posts, db = db_func.update_tag(posts, db, issue_array[i], final_tag)
            if final_tag != 'Spam@gmail.com':
                print 'Attachment List'
                print attach_list           
                sent_mail.send_mail(final_tag,'#' + str(issue_array[i]) +' ' + subject[i], '#'+ str(issue_array[i]) + '\r\n' + s.join(text[i]), attach_list[issue_array[i]])
            else:
                mail.uid('STORE', uid[i], '+FLAGS', '(\Deleted)')
                mail.expunge()
        for i in range(len(subject_re)):
            re_text = subject_re[i]['body']
            print 'Re-text ', re_text
            if re_text is not None:
                re_text = re_text.split("\r\n")
            else:
                re_text = None
            if re_text is not None:
                final_tag = watson.get_classified_tag(re_text[0], False)
                posts, db, stu_mail = db_func.fetch(posts, db, subject_re[i]['issue_no'])
                # get from send the teacher's mail
                posts, db = db_func.update_status(posts, db, subject_re[i]['issue_no'], final_tag)
                if final_tag != 'spam':
                    sent_mail.send_mail(stu_mail[u'from'],subject_re[i]['sub'],s.join(re_text) + '\r\n' + 'Please Fill  out this google Feedback form \r\n'+'https://docs.google.com/forms/d/e/1FAIpQLScVHY1rrdODF162mju7jzkcq-aFSvfo_-dhCJh_t9Louhk-yA/viewform?c=0&w=1 '+'\r\n\r\n  <             This is a Machine Generated Response.PLEASE DO NOT REPLY >', None)   
                else:
                    print 'spam detected'
        now = datetime.datetime.now()
        if  now.day == 1 and now.hour == 12 and now.minutes == 01:
            mail_dict = {1:{ "comp":0 ,"op":0 },2:{ "comp":0 ,"op":0 },3:{ "comp":0 ,"op":0 },4:{ "comp":0 ,"op":0 },5:{ "comp":0 ,"op":0 }}
            posts, db = db_func.it(posts, db, mail_dict)
                
if __name__ == '__main__':
    main()  