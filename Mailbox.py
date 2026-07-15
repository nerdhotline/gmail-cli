import json

from Mail import Mail 
from MailHeader import emailIdTime

class Mailbox:
  def __init__(self, apiService):
    self.collection:list[Mail] = []
    self.idLst = []
    self.apiService = apiService
 
    
  def setCollection(self, value):
    self.collection = value
  
  def setIdLst(self, value):
    self.idLst = value
  
  def sortIdLst(self):
    queryCollection = []
    lngth = len(self.idLst)
    for i in range(0, lngth):
      idObj = self.idLst[i]
      query = self.apiService.users().messages().get(
        userId="me", 
        id=idObj["id"],
        format="metadata"
      ).execute()

      newIdObj:emailIdTime = {
        "id": query.get("id", None),
        "threadId": query.get("threadId", None),
        "internalDate": query.get("internalDate", None)
      }
      queryCollection.append(newIdObj)
  

  def processMessages(messages:list, service:any) -> list[Mail]:
    result:list[Mail] = []
    for message in messages:
      msg = Mail(service, message)
      result.append(msg)
    return result
  
  
      