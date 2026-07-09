import base64
import json 

class Mail:
  def __init__(self, service, message):
    self.service = service
    self.message = self.service.users().messages().get(
      userId="me", 
      id=message["id"],
      format="full"
    ).execute()
    self.header = Mail.processHeader(self.message)
    self.body = Mail.processBody(self.message)

  def getMessage(self):
    return self.message
  
  def getHeader(self, value):
    return self.header

  # CLASS METHODS ------------------------------------------------------------------------------------------

  def processHeader(message):
    header, result = {}, {}
    wantedValues = ["Delivered-To", "Return-Path", "Date", "Subject", "From", "To", "Sender", "Reply-To"]
    result["id"] = message.get("id")
    result["threadId"] = message.get("threadId", None)
    result["labelIds"] = message.get("labelIds", None)
    result["snippet"] = message.get("snippet", None)
    result["internalDate"] = message.get("internalDate", None)

    header = message["payload"]["headers"]
    for itm in header:
      if itm["name"] in wantedValues:
        result[itm["name"].lower()] = itm["value"]
    return result



  def processBody(message):
    try:
      parts = message["payload"]["parts"]
      data = ""
      for part in parts:
        data += part["body"]["data"]

      decodedBytes = base64.urlsafe_b64decode(data)
      decodedText = decodedBytes.decode('utf-8').strip()

      return decodedText
    except KeyError:
      return "FAIL"
    

