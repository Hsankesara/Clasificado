import watson_access as watson
import api_google as api
import time
def main():
    while 1:    
        subject, text = api.check_new_mail()
        t = None
        if text is not None:
        	text = text.split("\r\n")
        	if subject is not None:
        		subject_tag = watson.get_classified_tag(subject, True)
			watson.get_classified_tag(text, True)
        time.sleep(120)

if __name__ == '__main__':
    main()