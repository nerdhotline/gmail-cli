from backend.mainImports import *
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer



# Authentication
gmailApi = ApiService(["https://www.googleapis.com/auth/gmail.readonly"])
gmailApi.refreshCreds()
service = gmailApi.buildApiService()
emailIDs = gmailApi.collectIdBatch()




class TableApp(App):
  BINDINGS = [
    ("d", "toggle_dark", "Toggle dark mode"), 
    ("q", "quit_app", "Terminate application")
  ]

  def compose(self) -> ComposeResult:
    yield DataTable()
    yield Footer()

  def on_mount(self) -> None:
    table = self.query_one(DataTable)
    table.add_columns('from', 'subject')
    for i in range(0, 50):
      itm = emailIDs[i]
      email = Mail(service, itm)
      frm = email.header["from"]
      subject = email.header["subject"]

      table.add_row(frm, subject)
  
  # EVENTS
  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
    self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")
  
  def action_quit(self) -> None:
    exit(29)

app = TableApp()
app.run()