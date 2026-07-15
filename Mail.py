import base64
from datetime import datetime
import json 
from MailHeader import GmailHeader
import tkinter as tk
from tkinterweb import HtmlFrame # import the HtmlFrame widget

class Mail:
  def __init__(self, service, message):
    self.service = service
    self.message = self.service.users().messages().get(
      userId="me", 
      id=message["id"],
      format="full"
    ).execute()
    self.header = self.processHeader()
    self.body = self.processBody()

  def getMessage(self):
    return self.message
  
  def getHeader(self, value):
    return self.header

  # CLASS METHODS ------------------------------------------------------------------------------------------

  def formatEmail(self):
    # Header
    print(f"from: {self.header["from"]}")
    print(f"date: {self.header["formattedDate"]}")
    print(f"mimeType: {self.header["mimeType"]}")

    # Body
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
    else:
      print(self.body)  
    print()
    




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
        for part in parts:
          if (part["mimeType"] == "text/html"):
            data += part["body"]["data"]
      elif (mimeType == "multipart/mixed"):
        for part in parts:
          if (part["mimeType"] == "multipart/related"):
            section = part["parts"]
            for sec in section:
              if(sec["mimeType"] == "text/html"):
                data += sec["body"]["data"]

      else:
        for part in parts:
          data += part["body"]["data"]

      decodedBytes = base64.urlsafe_b64decode(data)
      decodedText = decodedBytes.decode('utf-8').strip()

      return decodedText
    except KeyError:
      return "FAIL"
    

