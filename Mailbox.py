import json
import time

from Mail import Mail 
from MailHeader import emailIdTime
from concurrent.futures import ThreadPoolExecutor
import threading
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Mailbox:
  def __init__(self, apiService, creds):
    self.collection:list[Mail] = []
    self.idLst = []
    self.apiService = apiService
    self.creds = creds
    
  def setCollection(self, value):
    self.collection = value
  
  def setIdLst(self, value):
    self.idLst = value
  
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

  def processMessages(messages:list, service:any) -> list[Mail]:
    result:list[Mail] = []
    for message in messages:
      msg = Mail(service, message)
      result.append(msg)
    return result
  
  
      