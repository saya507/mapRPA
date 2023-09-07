from featureA.listmail import listmail
from featureB.normalize_address_chan import normalize_address
from featureB.normalize_address_road import normalize_address_v26
from featureB.memo_chan import get_map_pdf as get_map_pdf_chan
from featureB.memo_road import get_map_pdf as get_map_pdf_road
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

    #for message in messages_list:
        #print(research_address_chan = normalize_address(message["body"]))
        #print(research_address_road = normalize_address_v26(message["body"]))        
        # get_map_pdf_chan(research_address_chan)
        # get_map_pdf_road(research_address_road)
 
        # flag = "NG"
        # customer_address = message["from"]
        # pdf = "test.pdf"
      
        # sender = my_mail_address.my_mail_address
        # kick_main(flag,customer_address,pdf,sender)

main()

