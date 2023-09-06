from featureA.listmail import listmail
import json

def main():
    messages_json = listmail()
    messages_list = json.loads(messages_json)
    print("type:"+str(type(messages_list)))

    for message in messages_list:
        research_address = message["body"]
        mail_address = message["from"]

main()