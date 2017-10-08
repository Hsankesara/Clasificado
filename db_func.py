import sent_mail
def fetch(posts, db,issue_no):
     return (posts, db, posts.find_one({"issue_no" : issue_no}))

def update_tag(posts,db,issue_no,tag):
    print 'intial tag = ', posts.find_one({"issue_no": issue_no})[u'tag']
    db.posts.update_one({
        'issue_no': issue_no
    }, {
        '$set': {
            'tag'   :tag
        }
    }, upsert=False)
    print 'After Updating tags = ', posts.find_one({"issue_no": issue_no})[u'tag']
    return (posts,db)


def update_status( posts, db,issue_no,status):
    print 'initial status = ', posts.find_one({"issue_no": issue_no})[u'status']
    db.posts.update_one({
        'issue_no': issue_no
    }, {    
        '$set': {
            'status': status
        }
    }, upsert=False)
    print 'After updating status : ', posts.find_one({"issue_no": issue_no})[u'status']
    return (posts,db)

def it( posts,db, mail_dict):

    for p in posts.find({"tag":"diner.iiitv@gmail.com","status":"complete"}):
        mail_dict[1]["comp"] = mail_dict[1]["comp"] + 1


    for p in posts.find({"tag":"diner.iiitv@gmail.com"}):
        mail_dict[1]["op"]  = mail_dict[1]["op"] + 1


    for p in posts.find({"tag":"hec.iiitv@gmail.com","status":"complete"}):
        mail_dict[2]["comp"] = mail_dict[2]["comp"] + 1

    for p in posts.find({"tag":"hec.iiitv@gmail.com"}):
        mail_dict[2]["op"]  = mail_dict[2]["op"] + 1


    for p in posts.find({"tag":"cultural.iiitv@gmail.com","status":"complete"}):
        mail_dict[3]["comp"] = mail_dict[3]["comp"] + 1
    for p in posts.find({"tag":"cultural.iiitv@gmail.com"}):
        mail_dict[3]["op"]  = mail_dict[3]["op"] + 1

    for p in posts.find({"tag": "transport.iiitv@gmail.com", "status": "complete"}):
        mail_dict[4]["comp"] = mail_dict[4]["comp"] + 1
    for p in posts.find({"tag": "transport.iiitv@gmail.com"}):
        mail_dict[4]["op"] = mail_dict[4]["op"] + 1

    for p in posts.find({"tag":"academics.iiitv@gmail.com","status":"complete"}):
        mail_dict[5]["comp"] = mail_dict[5]["comp"] + 1
    for p in posts.find({"tag":"academics.iiitv@gmail.com"}):
        mail_dict[5]["op"]  = mail_dict[5]["op"] + 1
    
    completed, incompleted, opened = get_monthly_stats(mail_dict)
    sent_mail.send_mail('diner.iiitv@gmail.com', 'Your Monthly Stats','Total Opened :' + str(opened[1]) + '\r\nTotal Completed : ' + str(completed[1]) + '\r\nTotal InCompleted' + str(incompleted[1]) ,None )
    sent_mail.send_mail('hec.iiitv@gmail.com', 'Your Monthly Stats','Total Opened :' + str(opened[2]) + '\r\nTotal Completed : ' + str(completed[2]) + '\r\nTotal InCompleted' + str(incompleted[2]) ,None )
    sent_mail.send_mail('cultural.iiitv@gmail.com', 'Your Monthly Stats','Total Opened :' + str(opened[3]) + '\r\nTotal Completed : ' + str(completed[3]) + '\r\nTotal InCompleted' + str(incompleted[3]) ,None )
    sent_mail.send_mail('transport.iiitv@gmail.com', 'Your Monthly Stats','Total Opened :' + str(opened[4]) + '\r\nTotal Completed : ' + str(completed[4]) + '\r\nTotal InCompleted' + str(incompleted[4]) ,None )
    sent_mail.send_mail('academics.iiitv@gmail.com', 'Your Monthly Stats','Total Opened :' + str(opened[5]) + '\r\nTotal Completed : ' + str(completed[5]) + '\r\nTotal InCompleted' + str(incompleted[5]) ,None )
    
    print 'mails sent'
    return (posts, db)
def get_monthly_stats(mail_dict):

    x = mail_dict
    completed = []
    for i in range(5):
        completed.append(x[i+1]["comp"])
    opened = []
    for i in range(5):
        opened.append(x[i+1]["op"])
    incompleted = []
    for i in range(5):
         incompleted.append(x[i+1]["op"] - x[i+1]["comp"])

    clear_dict(mail_dict)

    print(completed)
    print(opened)
    print(incompleted)

    return (completed, incompleted, opened)

def clear_dict(mail_dict):   
    mail_dict.clear()