from featureA.listmail import listmail
from featureB.normalize_address_chan import normalize_address
from featureB.normalize_address_road import normalize_address_v26
from featureC import kick_main
import json
import featureC.__init__
import my_mail_address
import re

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
        research_address_chan = normalize_address(message["body"])
        research_address_road = normalize_address_v26(message["body"])
        print(message["body"])
        #print(research_address)

        # def BtoC(flag,customer_address,pdf):
        #     flag = "NG"
        #     customer_address = message["from"]
        #     pdf = "test.pdf"
        
        flag = "NG"
        customer_address = message["from"]
        print(customer_address)
        pdf = "test.pdf"
        # p = r'<(.+)>'
        # m = re.search(p,customer_address)
        # print(m.group(1))

        sender = "agroup0101@gmail.com"
        kick_main(flag,customer_address,pdf,sender)

main()

