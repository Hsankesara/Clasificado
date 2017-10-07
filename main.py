import watson_access as watson
import api_google as api
import time

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
    print subject_tag, body_tags
    return (subject_tag, body_tags)

def main():
    issue_number = 0
    while 1:
        issue_number, issue_array, subject, text = api.check_new_mail(issue_number)
        # Test get_tags
        #  subject = "regarding bus schedule"
        # text = """Sir, Our bus schedule is not according to our classes.\r\nSo many times we are facing difficulties to attend class.\r\nKindly cancel all the classes.\r\nwith regards\r\nHeet Sankesara"""
        for i in xrange(len(issue_array)):
            if text[i] is not None:
                text[i] = text[i].split("\r\n")
            else:
                text[i] = None
            subject_tag, body_tags = get_tags(subject[i], text[i], True)
            print issue_number
if __name__ == '__main__':
    main()