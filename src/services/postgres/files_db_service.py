from src.services.postgres.models.tables import Files

class FilesDbService:
  def __init__(self, db) -> None:
    self._db = db

  def add_file(self, custom_name, file_name, path):
    new_file = Files(custom_name=custom_name, file_name=file_name, path=path)
    self._db.transaction(lambda session: session.add(new_file))