import base64
from datetime import datetime
import json 
from backend.MailHeader import GmailHeader
import tkinter as tk
from tkinterweb import HtmlFrame # import the HtmlFrame widget
import re

class Mail:
  def __init__(self, service, message):
    self.service = service
    self.message = self.service.users().messages().get(
      userId="me", 
      id=message["id"],
      format="full"
    ).execute()
    self.header = self.processHeader()
    self.html = None
    self.body = self.processBody()
    

  def formatEmail(self):
    return f'''
    From: {self.header["from"]}
    Date: {self.header["formattedDate"]}
    Subject: {self.header["subject"]}

    {self.body}
    '''

  def getMessage(self):
    return self.message
  
  def getHeader(self, value):
    return self.header

  # CLASS METHODS ------------------------------------------------------------------------------------------

  def formatHeader(self):
    result = ''

    # Header
    result += f"from: {self.header["from"]}\n"
    result += f"date: {self.header["formattedDate"]}\n"
    result += f"mimeType: {self.header["mimeType"]}\n"

    return result

  def formatBody(self):
    result = ''

    # Body
    if (self.header["mimeType"] == "multipart/alternative"):
      # result += "[embedded html.]\n[see details]"
      result += f"\n{self.body}"
    # elif (self.header["mimeType"] == "multipart/mixed"):
    #   result += "[embedded html.]\n[see details]"
    else:
      result += f"\n{self.body}"  
    
    return result
  
  def renderEmail(self):
    if (self.header["mimeType"] == "multipart/alternative"):
      root = tk.Tk()
      frame = HtmlFrame(root, messages_enabled=False)
      frame.load_html(html_source=self.body)
      frame.pack(fill="both", expand=True)
      root.mainloop()
    elif (self.header["mimeType"] == "multipart/mixed"):
      root = tk.Tk()
      frame = HtmlFrame(root, messages_enabled=False)
      frame.load_html(html_source=self.body)
      frame.pack(fill="both", expand=True)
      root.mainloop()





  def processHeader(self):
    header, result, payload, wantedValues = {}, {}, {}, []

    payload = self.message["payload"] 
    
    # Parse Header Data
    header = self.message["payload"]["headers"]

    result: GmailHeader = {
      # Basic payload metadata
      "id": self.message.get("id", None),
      "threadId": self.message.get("threadId", None),
      "labelIds": self.message.get("labelIds", None),
      "snippet": self.message.get("snippet", None),
      "internalDate": self.message.get("internalDate", None),

      # Collect mimeType for body parsing
      "mimeType": payload.get("mimeType", None)
    }

    wantedValues = ["Delivered-To", "Return-Path", "Date", "Subject", "From", "To", "Sender", "Reply-To"]
    for itm in header:
      if itm["name"] in wantedValues:
        result[itm["name"].lower()] = itm["value"]

    # clean up "from" response [ex; someone <someone@email.com>]
    match = re.search(r"(.*?) <.*?>", result["from"])
    result["from"] = match.group(1) if match != None else result["from"]

    time = int(result["internalDate"])
    dtObj = datetime.fromtimestamp(time/1000)
    date = dtObj.strftime("%d/%m/%Y")
    result["formattedDate"] = date

    return result


  def processBody(self):
    try:
      mimeType = self.message["payload"]["mimeType"]
      parts = self.message["payload"]["parts"]

      data = ""
      if (mimeType == "multipart/alternative"):
        temp = ''
        for part in parts:
          if (part["mimeType"] == "text/html"):
            data += part["body"]["data"]
          if (part["mimeType"] == "text/plain"):
            temp += part["body"]["data"]

        decodedBytes = base64.urlsafe_b64decode(data)
        decodedText = decodedBytes.decode('utf-8').strip()
        self.html = decodedText

        decodedBytes = base64.urlsafe_b64decode(temp)
        decodedText = decodedBytes.decode('utf-8').strip()
        self.body = decodedText

        return decodedText

      elif (mimeType == "multipart/mixed"):
        temp = ''
        for part in parts:
          if (part["mimeType"] == "multipart/related"):
            section = part["parts"]
            for sec in section:
              if(sec["mimeType"] == "text/html"):
                data += sec["body"]["data"]
              if (part["mimeType"] == "text/plain"):
                temp += part["body"]["data"]
        decodedBytes = base64.urlsafe_b64decode(data)
        decodedText = decodedBytes.decode('utf-8').strip()
        self.html = decodedText

        decodedBytes = base64.urlsafe_b64decode(temp)
        decodedText = decodedBytes.decode('utf-8').strip()
        self.body = decodedText
        return decodedText

      else:
        for part in parts:
          data += part["body"]["data"]

        decodedBytes = base64.urlsafe_b64decode(data)
        decodedText = decodedBytes.decode('utf-8').strip()
        return decodedText
    except KeyError:
      return "FAIL"
    

