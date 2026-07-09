from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os.path


class Security:
  def __init__(self, SCOPES):
    self.SCOPES = SCOPES
    self.tknFilepath = "token.json"
    self.credsFilepath = "credentials.json"
  
  def grabCredentials(self):
    creds = None
    
    if os.path.exists(self.tknFilepath):
      creds = Credentials.from_authorized_user_file(self.tknFilepath, self.SCOPES)

    if (not creds or not creds.valid):
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
        creds = flow.run_local_server(port=0)

      with open(self.tknFilepath, "w") as token:
        token.write(creds.to_json())

    return creds

  def collectMessages(self, creds):
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = (
      service.users().messages().list(
        userId="me", 
        q="category:primary",
        labelIds=["INBOX"]
      ).execute()
    )

    messages = results.get("messages", [])

    # TODO: test no messages catch
    # TODO: remedy forced exit 
    if not messages:
      print("No messages found.")
      exit(29)  
    return messages, service