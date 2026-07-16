import json
import time

from backend.Mail import Mail 
from backend.MailHeader import emailIdTime
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
  
  

  def processMessages(messages:list, service:any) -> list[Mail]:
    result:list[Mail] = []
    for message in messages:
      msg = Mail(service, message)
      result.append(msg)
    return result
  
  
      