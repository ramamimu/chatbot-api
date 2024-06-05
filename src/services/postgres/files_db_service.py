from typing import List, Type
from src.exceptions.invariant_error import InvariantError
from src.services.postgres import PostgresDb
from src.services.postgres.models.tables import Files
from src.exceptions.not_found_error import NotFoundError

from sqlalchemy.sql import and_

class FilesDbService:
  def __init__(self, db) -> None:
    self._db: Type[PostgresDb] = db

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
  
  def get_file_by_id(self, id):
    session = self._db.get_session()
    try:
      file = session.query(Files).filter(Files.id == id).first()

      if not file:
        raise InvariantError("file not found")

      return file
    except:
      raise InvariantError("error when get file")
    finally:
      session.close()

  def get_files_by_id(self, files_id: List[str]):
    session = self._db.get_session()
    try:
      files = session.query(Files).filter(Files.id.in_(files_id)).all()

      if not files:
        raise InvariantError("files not found")

      return files
    except:
      raise InvariantError("error when get file")
    finally:
      session.close()

  def delete_file_by_id(self, id):
    self._db.transaction(lambda session: session.query(Files).filter(Files.id == id).delete())

  def delete_file_by_path(self, path):
    self._db.transaction(lambda session: session.query(Files).filter(Files.path == path).delete())
  
  def verify_file_by_id(self, id):
    session = self._db.get_session()
    try:
      file = session.query(Files).filter(Files.id == id).first()
      if not file:
        raise NotFoundError("file not exist").throw()
      return file
    except Exception as e:
      raise NotFoundError("error while verify file").throw()
    finally:
      session.close()

  def verify_file_by_id_name(self, id, name):
    session = self._db.get_session()
    try:
      file = session.query(Files).filter(and_(Files.id == id, Files.custom_name == name)).first()
      return file
    except:
      raise NotFoundError("name or id not exist").throw()
    finally:
      session.close()
  
  def get_all_files(self):
    session = self._db.get_session()
    try:
      files = session.query(Files).all()
      return files
    except Exception as e:
      raise NotFoundError("error while get files").throw()
    finally:
      session.close()
  
  async def verify_all_file_names_exist(self, file_names):
      session = self._db.get_session()
      try:
          # Query all files that match the names in the list
          files = session.query(Files).filter(Files.custom_name.in_(file_names)).all()
          
          # Check if all provided file names exist
          existing_file_names = {file.custom_name for file in files}
          for file_name in file_names:
              if file_name not in existing_file_names:
                  raise NotFoundError(f"File name '{file_name}' does not exist").throw()

          return files
      except Exception as e:
          raise NotFoundError("Error while verifying file names").throw()
      finally:
          session.close()

