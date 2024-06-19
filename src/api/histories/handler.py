class HistoriesHandler:
  def __init__(self, memorystore_service) -> None:
    self._memorystore_service = memorystore_service
  
  async def get_history_handler(self):
    return {"status": "success", "history": self._memorystore_service.get_all_memory()}

  async def get_history_list_handler(self):
    return  {"status": "success", "historyKeys": list(self._memorystore_service.get_all_memory().keys())} 

  async def get_history_by_id_handler(self, history_id):
    return {"status": "success", "history": self._memorystore_service.get_memory_with_handler(history_id)}

  async def delete_history_by_id_handler(self, history_id):
    self._memorystore_service.delete_memory_by_id(history_id)
    return {"detail": f"success to delete history chat"}

  async def delete_history_handler(self):
    self._memorystore_service.delete_all_memory()
    return {"detail": f"success to reset all history chat"}
