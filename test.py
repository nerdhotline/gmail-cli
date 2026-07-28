from backend.mainImports import *
from textual.screen import ModalScreen
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Static, Label
from textual.containers import Grid

# Authentication
gmailApi = ApiService(["https://www.googleapis.com/auth/gmail.readonly"])
gmailApi.refreshCreds()
service = gmailApi.buildApiService()
emailIDs = gmailApi.collectIdBatch()
mailbox = Mailbox()


for i in range(0, 50):
  itm = emailIDs[i]
  email = Mail(service, itm)
  print(json.dumps(email.message, indent=4))
  exit()




