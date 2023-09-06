##メール送信機能

from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import build
import smtplib
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
import mimetypes
from apiclient import errors
# from gmail_credential import get_credential
from docopt import docopt
import logging
import gmail_credential

logger = logging.getLogger(__name__)


##ーメール作成から下書き保存までー##
#APIのスコープを設定(どのAPIを使うのかの設定)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

##アクセストークンの取得
def get_credential():
    launch_browser = True
    flow = InstalledAppFlow.from_client_secrets_file("../client_id.json", SCOPES)
    flow.run_local_server()
    cred = flow.credentials
    return cred

##下書きの作成
def create_message(sender, to, subject, message_text):
    enc = "utf-8"
    message = MIMEText(message_text.encode(enc), _charset=enc)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}

##下書きフォルダに保存
def create_draft(service, user_id, message_body):
    message = {'message':message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()
    return draft

##実行
def main(sender, to, subject, message_text):
    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    message = create_message(sender, to, subject, message_text)
    create_draft(service, "me", message)



if __name__ == "__main__":
    sender = "a211410n@gmail.com"
    to = "a211410n@gmail.com"
    subject = "件名"
    message_text = "本文"
    main(sender=sender, to=to, subject=subject, message_text=message_text)


##ー下書き済みのメールを送信するー##
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def send_message(service, user_id, message):
    try:
        sent_message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        logger.info("Message Id: %s" % sent_message["id"])
        return None
    except errors.HttpError as error:
        logger.info("An error occurred: %s" % error)
        raise error

#  メイン処理
def main(sender, to, subject, message_text, attach_file_path, cc=None):
    # アクセストークンの取得とサービスの構築
    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    if attach_file_path:
        # メール本文の作成
        message = create_message_with_attachment(
            sender, to, subject, message_text, attach_file_path, cc=cc
        )
    else:
        message = create_message(
            sender, to, subject, message_text, cc=cc
        )
    # メール送信
    send_message(service, "me", message)

# プログラム実行部分
if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1")
    sender = arguments["<sender>"]
    to = arguments["<to>"]
    cc = arguments["--cc"]
    subject = arguments["<subject>"]
    message_text_file_path = arguments["<message_text_file_path>"]
    attach_file_path = arguments["--attach_file_path"]

    logging.basicConfig(level=logging.DEBUG)

    with open(message_text_file_path, "r", encoding="utf-8") as fp:
        message_text = fp.read()

    main(
        sender=sender,
        to=to,
        subject=subject,
        message_text=message_text,
        attach_file_path=attach_file_path,
        cc=cc,
    )








# ##1 正常に実行された場合、ユーザーに正しくPDFが送信される
# ##　!!!　テスト用PDFを作ってやってみる。
# if result == true:
#     sender = "a211410n@gmail.com"
#     to = "a211410n@gmail.com" #お客さんのアドレス（変数：cusAdr）
#     subject = "地図取得成功"
#     message_text = "地図が取得できました。{PDF}"
#     main(sender=sender, to=to, subject=subject, message_text=message_text)

# ##2 失敗時にユーザーにメールでエラーが通知される
# ##4 取得できなかった理由（住所入力が正しくない、対象地域外など）がユーザーに通知される
# if result == false:
#     sender = "a211410n@gmail.com"
#     to = "a211410n@gmail.com" #お客さんのアドレス（変数：cusAdr）
#     subject = "地図取得失敗"
#     message_text = "地図ができませんでした。" ##Bで関数に入れたテキストを代入？
#     main(sender=sender, to=to, subject=subject, message_text=message_text)

# ##3 一部のPDFが取得できなかった場合、そのことがユーザーに通知され、取得されたPDFは送信される
# ##4 取得できなかった理由（住所入力が正しくない、対象地域外など）がユーザーに通知される
# if result == little:
#     sender = "a211410n@gmail.com"
#     to = "a211410n@gmail.com" #お客さんのアドレス（変数：cusAdr）
#     subject = "地図取得一部成功"
#     message_text = "取得できた地図はこちらです。{PDF}取得できなかった地図はこちらです。{原因}" ##Bで関数に入れたテキストを代入？
#     main(sender=sender, to=to, subject=subject, message_text=message_text)



##5 ユーザーへの通知を見やすくする（html形式）