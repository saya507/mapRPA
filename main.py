from featureA.listmail import listmail
import json
import featureC.__init__
from featureC import kick_main
import my_mail_address

def main():
    messages_json = listmail()
    #print("type:"+str(type(messages_json)))

    if(messages_json):
        messages_list = json.loads(messages_json)
        #print("type:"+str(type(messages_list)))
    else:
        print("error in listmail.py")
        return

    for message in messages_list:
        research_address = message["body"]
        
        flag = "false"
        customer_address = message["from"]
        pdf = "test.pdf"
        sender = my_mail_address.my_mail_address
        kick_main(flag,customer_address,pdf,sender)

main()
