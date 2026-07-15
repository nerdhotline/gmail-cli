from Mail import Mail 

class Mailbox:
  def __init__(self):
    self.collection:list[Mail] = [] 
    
  def setCollection(self, value):
    self.collection = value
  
  def processMessages(messages:list, service:any) -> list[Mail]:
    result:list[Mail] = []
    for message in messages:
      msg = Mail(service, message)
      result.append(msg)
    return result
  
  
      