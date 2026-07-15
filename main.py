from mainImports import *


def run():
  try:
    # Authentication
    gmail_api = Security(["https://www.googleapis.com/auth/gmail.readonly"])
    creds = gmail_api.grabCredentials()
  
    idObjects, service = gmail_api.collectEmailIds(creds)

    mailbox = Mailbox(service)
    mailbox.setIdLst(idObjects)
    mailbox.sortIdLst()
    print('force-exit[main.py|15-16]')
    exit(8)
    mailbox.setCollection(Mailbox.processMessages(idObjects, service))

    
    
  except HttpError as error:
    # TODO - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  run()