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


class EmailScreen(ModalScreen):
  # CONTEXT ------------------------------------------------------------------------------------------------------------------------------------
  BINDINGS = [
    ("escape", "app.pop_screen", "Pop screen")
  ]
  CSS_PATH = "main.tcss"

  # --------------------------------------------------------------------------------------------------------------------------------------------
  def __init__(self, email:Mail, id:str):
    self.email = email
    super().__init__(id=id)

  def compose(self) -> ComposeResult:
    yield Footer()
    yield Grid(  
      Static(f"{self.email.header['subject']}", id="emailBox-subject"),
      Static(f"{self.email.formatHeader()}", id="emailBox-metadata"),
      Static(f"{self.email.formatBody()}", id="emailBox-body"),
      id="emailBox"   
    )


class TableApp(App):
  # CONTEXT ------------------------------------------------------------------------------------------------------------------------------------
  SCREENS = {
    "email_screen": EmailScreen
  }

  CSS_PATH = "main.tcss"
  BINDINGS = [
    ("d", "toggle_dark", "Toggle dark mode"), 
    ("q", "quit_app()", "Terminate application"),
    ("b", "push_screen('email_screen')", "Switch"),
    ("enter", "selected_email()", "Select")
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
  
  def action_quit_app(self) -> None:
    self.exit()
  
  def action_selected_email(self) -> None:
    if self.cursor_row is not None and self.cursor_row >= 0:
      # Grab the row key corresponding to the current cursor position
      row_key, _ = self.coordinate_to_cell_key(self.cursor_coordinate)
      
      # Post the RowSelected message manually
      self.post_message(
        self.RowSelected(self, self.cursor_row, row_key)
      )
  
  # EVENTS -------------------------------------------------------------------------------------------------------------------------------------
  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
    self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")
  
  def on_data_table_row_selected(self, event:DataTable.RowSelected):
    selectedEmail:Mail = mailbox.idLst[event.row_key]
    self.push_screen(EmailScreen(selectedEmail, id="MyScreen"))

app = TableApp()
app.run()