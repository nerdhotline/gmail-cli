from textual.app import App, ComposeResult, Widget, RenderResult
from textual.widgets import Footer, Header, Static
from mainImports import *

class Hello(Widget):
    def render(self, test) -> RenderResult:
        return test


class StopwatchApp(App):
  """A Textual app to manage stopwatches."""  
  BINDINGS = [
    ("q", "quit", "Quit the app"),
    ("d", "toggle_dark", "Toggle dark mode")
  ]
  

  
  

  def compose(self) -> ComposeResult:
    """Create child widgets for the app."""
    # yield Header()
    yield Static(id="text")
    yield Footer()

  def on_mount(self) -> None:
    self.keyTable = {}
    try:
      # Authentication
      gmail_api = Security(["https://www.googleapis.com/auth/gmail.readonly"])
      creds = gmail_api.grabCredentials()
      messages, service = gmail_api.collectMessages(creds)

      # Read Messages
      for message in messages:
        msg = Mail(service, message)
        self.keyTable["msg"] = msg.body
        time = int(msg.header["internalDate"])
        dtObj = datetime.fromtimestamp(time/1000)
        date = dtObj.strftime("%d/%m/%Y")

        TEXT = f"""\

        from: {msg.header["from"]}
        date: {date}
        [@click=app.tryRender("msg")]Click Me[/]
        """

        temp = self.query_one("#text", Static)
        temp.update(TEXT)


        
        
        break

      
    except HttpError as error:
      # TODO - Handle errors from gmail API.
      print(f"An error occurred: {error}")



  
  def action_tryRender(self, msg):
    root = tk.Tk()
    frame = HtmlFrame(root, messages_enabled=False)
    frame.load_html(html_source=self.keyTable[msg])
    frame.pack(fill="both", expand=True)
    root.mainloop()
    
  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
          
    self.theme = (
      "textual-dark" if self.theme == "textual-light" else "textual-light"      
    )

if __name__ == "__main__":  
  app = StopwatchApp()
  app.run()