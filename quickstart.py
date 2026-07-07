import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


import json 
import re
import base64
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import html2text

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def grabCredentials():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
      token.write(creds.to_json())

  return creds

def collectMessages(creds):
  # Call the Gmail API
  service = build("gmail", "v1", credentials=creds)
  results = (
    service.users().messages().list(
      userId="me", labelIds=["INBOX"]
    ).execute()
  )
  messages = results.get("messages", [])

  # TODO: test no messages catch
  # TODO: remedy forced exit 
  if not messages:
    print("No messages found.")
    exit(29)  
  return messages, service



def main():
  creds = grabCredentials()
  try:
    messages, service = collectMessages(creds)


    
    for message in messages:
      msg = (
        service.users().messages().get(
          userId="me", 
          id=message["id"]
        ).execute()
      )

      if(msg["payload"]["body"]["size"] == 0):
        continue
      print(f'Message ID: {message["id"]}')
      
      raw_body_data = msg["payload"]["body"]["data"]
      decoded_bytes = base64.urlsafe_b64decode(raw_body_data)
      decoded_text = decoded_bytes.decode('utf-8').strip()
      decoded_text = re.sub(r'<!-- == Footer Section == -->[\s\S]*', '', decoded_text)

      h = html2text.HTML2Text()
      h.ignore_links = True

      console = Console(width=100)
      markdown_text = html2text.html2text(decoded_text)
      console.print(Panel(Markdown(markdown_text.replace("|", ''), )))
      print(f'  Subject: {msg["snippet"]}')

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()