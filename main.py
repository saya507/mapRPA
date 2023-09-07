from featureA.listmail import listmail
import json
import featureC.__init__
from featureC import kick_main
from . import my_mail_address

def main():
    messages_json = listmail()
    messages_list = json.loads(messages_json)
    print("type:"+str(type(messages_list)))

    for message in messages_list:
        research_address = message["body"]
        
        flag = "false"
        customer_address = message["from"]
        pdf = "test.pdf"
        sender = my_mail_address.my_mail_address
        kick_main(flag,customer_address,pdf,sender)

main()
