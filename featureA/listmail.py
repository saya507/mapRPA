
"""
list GMail Inbox.

Usage:
  listmail.py <query> <tag> <count>
  listmail.py -h | --help
  listmail.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
import pickle
import base64
import json
import io
import csv
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
from apiclient import errors
import logging
from docopt import docopt
from featureA.gmail_credential import get_credential
#gmail_credential import get_credential

logger = logging.getLogger(__name__)


def list_labels(service, user_id):
    """
    label のリストを取得する
    """
    labels = []
    response = service.users().labels().list(userId=user_id).execute()
    return response["labels"]


def decode_base64url_data(data):
    """
    base64url のデコード
    """
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode("UTF-8")
    return decoded_message


def list_message(service, user_id, query, label_ids=[], count=3):
    """
    メールのリストを取得する

    Parameters
    ----------
    service : googleapiclient.discovery.Resource
        Gmail と通信するためのリソース
    user_id : str
        利用者のID
    query : str
        メールのクエリ文字列。 is:unread など
    label_ids : list
        検索対象のラベルを示すIDのリスト
    count : str
        リターンするメール情報件数の上限

    Returns
    ----------
    messages : list
        id, body, subject, from などのキーを持った辞書データのリスト
    """
    messages = []
    try:
        message_ids = (
            service.users()
            .messages()
            .list(userId=user_id, maxResults=count, q=query, labelIds=label_ids)
            .execute()
        )

        if message_ids["resultSizeEstimate"] == 0:
            logger.warning("no result data!")
            return []

        # message id を元に、message の内容を確認
        for message_id in message_ids["messages"]:
            message_detail = (
                service.users()
                .messages()
                .get(userId="me", id=message_id["id"])
                .execute()
            )
            message = {}
            message["id"] = message_id["id"]
            # 単純なテキストメールの場合
            if 'data' in message_detail['payload']['body']:
                message["body"] = decode_base64url_data(
                    message_detail["payload"]["body"]["data"]
                )
            # html メールの場合、plain/text のパートを使う
            else:
                parts = message_detail['payload']['parts']
                # print(parts[0])
                parts = [part for part in parts if part['mimeType'] == 'text/plain']
                if len(parts) == 0:
                    continue        
                message["body"] = decode_base64url_data(
                    parts[0]['body']['data']
                    )
            # payload.headers[name: "Subject"]
            message["subject"] = [
                header["value"]
                for header in message_detail["payload"]["headers"]
                if header["name"] == "Subject"
            ][0]
            # payload.headers[name: "From"]
            message["from"] = [
                header["value"]
                for header in message_detail["payload"]["headers"]
                if header["name"] == "From"
            ][0]
            logger.info(message_detail["snippet"])
            messages.append(message)
        return messages

    except errors.HttpError as error:
        print("An error occurred: %s" % error)


def remove_labels(service, user_id, messages, remove_labels):
    """
    ラベルを削除する。既読にするために利用(is:unread ラベルを削除すると既読になる）
    """
    message_ids = [message["id"] for message in messages]
    labels_mod = {
        "ids": message_ids,
        "removeLabelIds": remove_labels,
        "addLabelIds": [],
    }
    # import pdb;pdb.set_trace()
    try:
        message_ids = (
            service.users()
            .messages()
            .batchModify(userId=user_id, body=labels_mod)
            .execute()
        )
    except errors.HttpError as error:
        print("An error occurred: %s" % error)

def add_labels(service, user_id, messages, processed_labels):
    """
    todo:ラベルを追加する。
    """
    message_ids = [message["id"] for message in messages]
    labels_mod = {
        "ids": message_ids,
        "removeLabelIds": processed_labels,
        "addLabelIds": [],
    }
    # import pdb;pdb.set_trace()
    try:
        message_ids = (
            service.users()
            .messages()
            .batchModify(userId=user_id, body=labels_mod)
            .execute()
        )
    except errors.HttpError as error:
        print("An error occurred: %s" % error)


# メイン処理
def main(query="is:unread", tag="daily_report", count=3):
    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    # ラベル一覧
    labels = list_labels(service, "me")
    #print("labels="+str(len(labels)))
    target_label_ids = [label["id"] for label in labels if label["name"] == tag]
    
    # メール一覧 [{'body': 'xxx', 'subject': 'xxx', 'from': 'xxx'},]
    #messages = list_message(service, "me", query, target_label_ids, count=count)
    messages = list_message(service, "me", query, "UNREAD", count=count)

    # unread label
    unread_label_ids = [label["id"] for label in labels if label["name"] == "UNREAD"]

    # remove labels form messages
    #remove_labels(service, "me", messages, remove_labels=unread_label_ids)
    logger.info(json.dumps(messages, ensure_ascii=False))
    if messages:
        return json.dumps(messages, ensure_ascii=False)
    else:
        return None

    #todo: 処理済みであることを示すラベルを追加
    # add_labels(service, "me", messages, add_labels=unread_label_ids)
    # logger.info(json.dumps(messages, ensure_ascii=False))
    # if messages:
    #     return json.dumps(messages, ensure_ascii=False)
    # else:
    #     return None

# プログラム実行部分
if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1")
    query = arguments["<query>"]
    tag = arguments["<tag>"]
    count = arguments["<count>"]
    logging.basicConfig(level=logging.DEBUG)

    messages_json = main(query=query, tag=tag, count=count)
    messages_list = json.loads(messages_json)
    print("type:"+str(type(messages_list)))
    print(messages_list[0].keys())
    print(messages_list[0]["subject"] )
    #print(f"messages_json: \n{messages_json}")

    for message in messages_list:
         print(message["subject"])

def listmail():
    query = "is:unread"
    tag = "UNREAD"
    count = 10
    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    # ラベル一覧
    labels = list_labels(service, "me")

    #target_label_subject_ids = []
    target_label_ids = [label["id"] for label in labels if label["name"] == tag]
    
    # メール一覧 [{'body': 'xxx', 'subject': 'xxx', 'from': 'xxx'},]
    messages = list_message(service, "me", query, target_label_ids, count=count)
    #messages = list_message(service, "me", query, target_label_subject_ids, count=count)

    # unread label
    unread_label_ids = [label["id"] for label in labels if label["name"] == "UNREAD"]

    # remove labels form messages
    remove_labels(service, "me", messages, remove_labels=unread_label_ids)
    logger.info(json.dumps(messages, ensure_ascii=False))
    if messages:
        return json.dumps(messages, ensure_ascii=False)
    else:
        return None

