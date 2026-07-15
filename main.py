from mainImports import *


def run():
  try:
    # Authentication
    gmail_api = Security(["https://www.googleapis.com/auth/gmail.readonly"])
    creds = gmail_api.grabCredentials()
    messages, service = gmail_api.collectMessages(creds)
    mailbox = Mailbox()
    mailbox.setCollection(Mailbox.processMessages(messages, service))

    
    
  except HttpError as error:
    # TODO - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  run()