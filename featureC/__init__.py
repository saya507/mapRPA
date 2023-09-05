##メール送信機能


##1 正常に実行された場合、ユーザーに正しくPDFが送信される
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import build

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

##2 失敗時にユーザーにメールでエラーが通知される
##3 一部のPDFが取得できなかった場合、そのことがユーザーに通知され、取得されたPDFは送信される
##4 取得できなかった理由（住所入力が正しくない、対象地域外など）がユーザーに通知される
##5 ユーザーへの通知を見やすくする（html形式）