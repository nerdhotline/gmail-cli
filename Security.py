import json

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
    #TODO: Add timeout feature for creds
    creds = None

    if os.path.exists(self.tknFilepath):
      creds = Credentials.from_authorized_user_file(self.tknFilepath, self.SCOPES)

    if (not creds or not creds.valid):
      print('tickticktick')
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
        creds = flow.run_local_server(port=0)

      with open(self.tknFilepath, "w") as token:
        token.write(creds.to_json())

    return creds

  def collectMessages(self, creds):
    queryCollection, query = [], None
    apiService, messages, nextPageToken = None, [], ''
    
    # build api service, collect all email id's 
    apiService = build("gmail", "v1", credentials=creds)  
    while (nextPageToken != None):
      query = (
        apiService.users().messages().list(
          userId="me", 
          labelIds=["INBOX"],
          pageToken=nextPageToken
        ).execute()  
      ) if (nextPageToken != '') else (
        # Parameter settings for initial query
        apiService.users().messages().list(
          userId="me", 
          labelIds=["INBOX"],
        ).execute()
      )
      messages = query.get("messages", []) #
      nextPageToken = query.get("nextPageToken", None)
      queryCollection += messages

    if (len(queryCollection) == 0):
      # TODO: test no messages catch
      # TODO: remedy forced exit 
      print("No messages found.")
      print("force-exit[Security.py, 59-60]")
      exit(60)  
      
    return queryCollection, apiService