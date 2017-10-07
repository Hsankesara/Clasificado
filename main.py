import watson_access as watson
import api_google as api
import time
def main():
    while 1:    
        text = api.check_new_mail()
        text.split('\n')
        watson.get_classified_tag(, True)
        time.sleep(120)

if __name__ == '__main__':
    main()