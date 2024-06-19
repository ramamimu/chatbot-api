from langchain_community.chat_message_histories import ChatMessageHistory

class MemorystoreService:
  def __init__(self) -> None:
    self._memorystore = {}

  def create_new_memory(self, id: str):
    self._memorystore[id] = ChatMessageHistory()
  
  def get_memory(self, id: str):
    if id not in self._memorystore:
      self.create_new_memory(id) 
    return self._memorystore[id]
  
  def add_user_message(self, id: str, message: str):
    if id not in self._memorystore:
      self.create_new_memory(id)
    
    self._memorystore[id].add_user_message(message)

  def add_ai_message(self, id: str, message: str):
    if id not in self._memorystore:
      self.create_new_memory(id)
    
    self._memorystore[id].add_ai_message(message)
