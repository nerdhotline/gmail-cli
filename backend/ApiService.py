import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os.path


class ApiService:
  def __init__(self, SCOPES):
    self.SCOPES = SCOPES
    self.tknFilepath = "token.json"
    self.credsFilepath = "credentials.json"
    self.creds = None
  
  def setCreds(self, value) -> None:
    self.creds = value
  
  def buildApiService(self):
    return build(
      serviceName="gmail", 
      version="v1", 
      credentials=self.creds
    )  


  def refreshCreds(self):
    #TODO: Add timeout feature for creds
    creds, flow = None, None

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

    self.setCreds(creds)

  

  def collectIdBatch(self, count:int=100, nextPageToken:str=''):
    queryCollection, query = [], None
    apiService, messages = None, []
    
    # build api service, collect all email id's 
    apiService = self.buildApiService()

    query = (
      apiService.users().messages().list(
        userId="me", labelIds=["INBOX"], maxResults=count,
      ).execute()  
    )

    messages = query.get("messages", [])
    queryCollection += messages
    return queryCollection


  def collectEmailIds(self):
    queryCollection, query = [], None
    apiService, messages, nextPageToken = None, [], ''
    
    # build api service, collect all email id's 
    apiService = self.buildApiService()
    while (nextPageToken != None):
      query = (
        apiService.users().messages().list(
          userId="me", 
          labelIds=["INBOX"],
          maxResults=500,
          pageToken=nextPageToken
        ).execute()  
      ) if (nextPageToken != '') else (
        # Parameter settings for initial query
        apiService.users().messages().list(
          userId="me", 
          labelIds=["INBOX"],
          maxResults=500
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
    
    def sortIdLst(self):
      def collectInternalDate(idObj:any) -> None:
        query, newIdObj = None, None

        # Ensure each thread has an apiService to make call on
        if (not hasattr (threadContext, "apiService")):
          threadContext.apiService = build("gmail", "v1", credentials=self.creds)
        
        try:
          query = threadContext.apiService.users().messages().get(
            userId="me", 
            id=idObj["id"],
            format="metadata"
          ).execute()

          newIdObj:emailIdTime = {
            "id": query.get("id", None),
            "threadId": query.get("threadId", None),
            "internalDate": query.get("internalDate", None)
          }
        except HttpError as e:
          print(e.resp.status)
          print(e.content)
          print(e.error_details)
          print('httpError-[Mailbox.py|collectInternalDate]')
          exit(46)

        return newIdObj


      start = time.perf_counter()
      queryCollection = []

      threadContext = threading.local()

      with ThreadPoolExecutor(max_workers=10) as executor:
        queryCollection = list(executor.map(collectInternalDate, self.idLst))

      end = time.perf_counter()
      print(f"{end - start:.6f}")
      print(len(queryCollection))
      
      return queryCollection, apiService