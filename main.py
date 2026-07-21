from backend.mainImports import *
from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Static

# Authentication
gmailApi = ApiService(["https://www.googleapis.com/auth/gmail.readonly"])
gmailApi.refreshCreds()
service = gmailApi.buildApiService()
emailIDs = gmailApi.collectIdBatch()
mailbox = Mailbox()


class EmailScreen(Screen):
  # CONTEXT ------------------------------------------------------------------------------------------------------------------------------------
  BINDINGS = [
    ("escape", "app.pop_screen", "Pop screen")
  ]

  # --------------------------------------------------------------------------------------------------------------------------------------------
  def __init__(self, header:dict, id:str):
    self.header = header
    super().__init__(id=id)

  def compose(self) -> ComposeResult:
    yield Static(f"{json.dumps(self.header, indent=4)}", id="BSOD_body")
    yield Footer()



class TableApp(App):
  # CONTEXT ------------------------------------------------------------------------------------------------------------------------------------
  SCREENS = {
    "email_screen": EmailScreen
  }

  BINDINGS = [
    ("d", "toggle_dark", "Toggle dark mode"), 
    ("q", "quit_app", "Terminate application"),
    ("b", "push_screen('email_screen')", "Switch")
  ]

  # --------------------------------------------------------------------------------------------------------------------------------------------
  def compose(self) -> ComposeResult:
    yield DataTable(cursor_type='row')
    yield Footer()

  def on_mount(self) -> None:
    table = self.query_one(DataTable)
    table.add_columns('from', 'subject')
    for i in range(0, 50):
      itm = emailIDs[i]
      email = Mail(service, itm)
      mailbox.setIdLst(email.header["id"], email)

      frm = email.header["from"]
      subject = email.header["subject"]

      table.add_row(frm, subject, key=itm["id"])
  
  # EVENTS -------------------------------------------------------------------------------------------------------------------------------------
  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
    self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")
  
  def on_data_table_row_selected(self, event:DataTable.RowSelected):
    selectedEmail:Mail = mailbox.idLst[event.row_key]
    self.push_screen(EmailScreen(selectedEmail.formatEmail(), id="MyScreen"))

app = TableApp()
app.run()