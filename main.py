from featureA.listmail import listmail
from featureB.normalize_address import normalize_address
from featureC import kick_main
import json
import featureC.__init__
import my_mail_address

def main():
    messages_json = listmail()
    #print("type:"+str(type(messages_json)))

    if(messages_json):
        messages_list = json.loads(messages_json)
        print("type:"+str(type(messages_list)))
        #print(messages_list[0]["body"])
    else:
        print("error in listmail.py")
        return

    for message in messages_list:
        research_address = normalize_address(message["body"])
        #print(research_address)
 
        flag = "NG"
        customer_address = message["from"]
        pdf = "test.pdf"
      
        sender = my_mail_address.my_mail_address
        kick_main(flag,customer_address,pdf,sender)

main()

