from featureA.listmail import listmail

from featureB.normalize_address_chan import normalize_address as normalize_address_chan
from featureB.normalize_address_road import normalize_address as normalize_address_road
from featureB.memo_chan import get_map_pdf as get_map_pdf_chan
from featureB.memo_road import get_map_pdf as get_map_pdf_road

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
    cnt = 0
    for message in messages_list:

        
        cnt += 1
        print("mail "+str(cnt))
        research_address_chan = normalize_address_chan(message["body"])
        research_address_road = normalize_address_road(message["body"])
        print(research_address_chan)
        print(research_address_road)        
        get_map_pdf_chan(research_address_chan, cnt)
        # get_map_pdf_road(research_address_road, cnt)
        
        # def BtoC(flag,customer_address,pdf):
        #     flag = "NG"
        #     customer_address = message["from"]
        #     pdf = "test.pdf"
        
        flag = "NG"
        customer_address = message["from"]
        print(customer_address)
        pdf = "ss/map_chan"+str(cnt)+".pdf"
        # p = r'<(.+)>'
        # m = re.search(p,customer_address)
        # print(m.group(1))
 
        
        sender = my_mail_address.my_mail_address
        kick_main(flag, customer_address, pdf, sender)


main()

