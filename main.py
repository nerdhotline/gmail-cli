from mainImports import *


def run():
  try:
    # Authentication
    gmail_api = Security(["https://www.googleapis.com/auth/gmail.readonly"])
    creds = gmail_api.grabCredentials()
    messages, service = gmail_api.collectMessages(creds)

    # Read Messages
    for message in messages:
      msg = Mail(service, message)
      msg.formatEmail()

      while(True):
        usrInput = input()
        if(usrInput == 'a'):
          break
        elif(usrInput == 'q'):
          exit(4)
      continue
    
  except HttpError as error:
    # TODO - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  run()