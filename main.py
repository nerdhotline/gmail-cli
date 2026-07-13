from googleapiclient.errors import HttpError
import json 
import re
import base64
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import html2text

from Mail import Mail
from Security import Security
from datetime import datetime


def main():
  try:
    # Authentication
    gmail_api = Security(["https://www.googleapis.com/auth/gmail.readonly"])
    creds = gmail_api.grabCredentials()
    messages, service = gmail_api.collectMessages(creds)

    # Read Messages
    for message in messages:
      msg = Mail(service, message)
      # print(json.dumps(msg.message, indent=4))
      # print(json.dumps(msg.header, indent=4))
      time = int(msg.header["internalDate"])
      dtObj = datetime.fromtimestamp(time/1000)
      date = dtObj.strftime("%d/%m/%Y")

      # format email
      print(f"from: {msg.header["from"]}")
      print(f"date: {date}")
      print()
      print(msg.body)

      exit(9)

    
  except HttpError as error:
    # TODO - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()