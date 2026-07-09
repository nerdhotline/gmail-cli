from googleapiclient.errors import HttpError


import json 
import re
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import html2text


def main():
  creds = grabCredentials()
  try:
    messages, service = collectMessages(creds)
    
    for message in messages:
      msg = (
        service.users().messages().get(
          userId="me", 
          id=message["id"],
          format="full"
        ).execute()
      )

      # # CUSTOM HEADER DATA
      header = msg["payload"]["headers"]
      wantedValues = ["Date", "Subject", "From", "To", "Sender", "Reply-To"]
      cstmHeader = {}

      for itm in header:
        if itm["name"] in wantedValues:
          cstmHeader[itm["name"].lower()] = itm["value"]
      
      cstmHeader["id"] = msg["id"]
      cstmHeader["threadId"] = msg["threadId"]
      cstmHeader["labelIds"] = msg["labelIds"]
      cstmHeader["snippet"] = msg["snippet"]

      print(json.dumps(msg, indent=2))

      raw_body_data = msg["payload"]["body"]["data"]



      decoded_bytes = base64.urlsafe_b64decode(raw_body_data)
      decoded_text = decoded_bytes.decode('utf-8').strip()
      decoded_text = re.sub(r'<!-- == Footer Section == -->[\s\S]*', '', decoded_text)

      h = html2text.HTML2Text()
      h.ignore_links = True
      markdown_text = html2text.html2text(decoded_text)

      console = Console(width=100)
      console.print(cstmHeader["subject"])
      console.rule()
      console.print(Panel(Markdown(markdown_text.replace("|", ''), )))

      exit(7)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()