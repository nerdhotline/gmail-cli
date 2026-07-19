from backend.mainImports import *


def run():
  try:
    # Authentication
    gmailApi = ApiService(["https://www.googleapis.com/auth/gmail.readonly"])
    gmailApi.refreshCreds()

    # collect email ID's via messages.list()
    emailIDs = gmailApi.collectIdBatch()
    



  

    
    
  except HttpError as error:
    # TODO - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  run()