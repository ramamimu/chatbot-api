from src.services.postgres.models.tables import Files
from sqlalchemy.sql import and_

class FilesDbService:
  def __init__(self, db) -> None:
    self._db = db

  def add_file(self, custom_name, file_name, path):
    new_file = Files(custom_name=custom_name, file_name=file_name, path=path)
    self._db.transaction(lambda session: session.add(new_file))

  def get_all_file(self):
    session = self._db.get_session()
    try:
      files = session.query(Files).all()
      return files
    finally:
      session.close()
  
  def delete_file_by_id(self, id):
    self._db.transaction(lambda session: session.query(Files).filter(Files.id == id).delete())

  def delete_file_by_path(self, path):
    self._db.transaction(lambda session: session.query(Files).filter(Files.path == path).delete())
  
  def verify_file_by_id_name(self, id, name):
    session = self._db.get_session()
    try:
      files = session.query(Files).filter(and_(Files.id == id, Files.custom_name == name))
      return files[0].file_name
    except Exception as e:
      raise Exception(e)
    finally:
      session.close()