from langchain_community.chat_message_histories import ChatMessageHistory
from src.exceptions.invariant_error import InvariantError

class MemorystoreService:
  def __init__(self) -> None:
    self._memorystore = {}

  def create_new_memory(self, id: str):
    self._memorystore[id] = ChatMessageHistory()

  def get_all_memory(self,):
    return self._memorystore

  def get_memory(self, id: str):
    if id not in self._memorystore:
      self.create_new_memory(id) 
    return self._memorystore[id]

  def get_memory_with_handler(self, id: str):
    if id not in self._memorystore:
      raise InvariantError("id not exist").throw()
    return self._memorystore[id]

  def add_user_message(self, id: str, message: str):
    if id not in self._memorystore:
      self.create_new_memory(id)
    self._memorystore[id].add_user_message(message)
  
  def delete_all_memory(self):
    self._memorystore.clear()

  def delete_memory_by_id(self, id: str):
    if id not in self._memorystore:
      raise InvariantError("id not exist").throw()
    del self._memorystore[id]

  def add_ai_message(self, id: str, message: str):
    if id not in self._memorystore:
      self.create_new_memory(id)
    self._memorystore[id].add_ai_message(message)
