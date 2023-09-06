from featureA.listmail import listmail
import json
import featureC.__init__
from featureC import kick_main

def main():
    messages_json = listmail()
    messages_list = json.loads(messages_json)
    print("type:"+str(type(messages_list)))

    for message in messages_list:
        research_address = message["body"]
        mail_address = message["from"]
        
        flag = "false"
        cus_address = mail_address
        pdf = "test.pdf"
        sender = ""
        kick_main(flag,cus_address,pdf,sender)

main()
