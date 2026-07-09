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



def main():
  creds = grabCredentials()
  try:
    messages, service = collectMessages(creds)
    
    for message in messages:
      msg = (
        service.users().messages().get(
          userId="me", 
          id=message["id"],
          format="full"
        ).execute()
      )

      # # CUSTOM HEADER DATA
      header = msg["payload"]["headers"]
      wantedValues = ["Date", "Subject", "From", "To", "Sender", "Reply-To"]
      cstmHeader = {}

      for itm in header:
        if itm["name"] in wantedValues:
          cstmHeader[itm["name"].lower()] = itm["value"]
      
      cstmHeader["id"] = msg["id"]
      cstmHeader["threadId"] = msg["threadId"]
      cstmHeader["labelIds"] = msg["labelIds"]
      cstmHeader["snippet"] = msg["snippet"]

      print(json.dumps(msg, indent=2))

      raw_body_data = msg["payload"]["body"]["data"]



      decoded_bytes = base64.urlsafe_b64decode(raw_body_data)
      decoded_text = decoded_bytes.decode('utf-8').strip()
      decoded_text = re.sub(r'<!-- == Footer Section == -->[\s\S]*', '', decoded_text)

      h = html2text.HTML2Text()
      h.ignore_links = True
      markdown_text = html2text.html2text(decoded_text)

      console = Console(width=100)
      console.print(cstmHeader["subject"])
      console.rule()
      console.print(Panel(Markdown(markdown_text.replace("|", ''), )))

      exit(7)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()