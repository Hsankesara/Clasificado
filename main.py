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
    while 1:    
        subject, text = api.check_new_mail()
        print subject, text
        # Test get_tags
        #  subject = "regarding bus schedule"
        # text = """Sir, Our bus schedule is not according to our classes.\r\nSo many times we are facing difficulties to attend class.\r\nKindly cancel all the classes.\r\nwith regards\r\nHeet Sankesara"""
        if text is not None:
            text = text.split("\r\n")
        else:
            text = None
        subject_tag, body_tags = get_tags(subject, text, True)
        time.sleep(120)

if __name__ == '__main__':
    main()