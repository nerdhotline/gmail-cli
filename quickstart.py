import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
  return messages, service



def main():
  creds = grabCredentials()
  try:
    messages, service = collectMessages(creds)

    if not messages:
      print("No messages found.")
      return

    print("Messages:")
    for message in messages:
      print(f'Message ID: {message["id"]}')
      msg = (
        service.users().messages().get(
          userId="me", 
          id=message["id"]
        ).execute()
      )
      print(f'  Subject: {msg["snippet"]}')

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()