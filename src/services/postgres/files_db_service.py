from sqlalchemy.sql import and_
import math

from src.services.postgres.models.tables import Files
from src.exceptions.invariant_error import InvariantError
from src.exceptions.not_found_error import NotFoundError

class FilesDbService:
  def __init__(self, db) -> None:
    self._db = db
    self._limit = 10

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
  
  def get_max_page(self):
    session = self._db.get_session()
    try:
      files = session.query(Files).count()
      return math.ceil(files/self._limit)
    finally:
      session.close()

  def get_file_by_offset(self, offset):
    print(offset * self._limit)
    session = self._db.get_session()
    try:
      files = session.query(Files).limit(self._limit).offset((offset - 1) * self._limit).all()
      return files
    finally:
      session.close()
  
  def get_file_by_id(self, id):
    session = self._db.get_session()
    try:
      file = session.query(Files).filter(Files.id == id).first()

      if not file:
        raise 

      return file
    except:
      session.rollback()
      raise InvariantError("file not found")
    finally:
      session.close()

  def delete_file_by_id(self, id):
    self._db.transaction(lambda session: session.query(Files).filter(Files.id == id).delete())

  def delete_file_by_path(self, path):
    self._db.transaction(lambda session: session.query(Files).filter(Files.path == path).delete())
  
  def verify_file_by_id(self, id):
    session = self._db.get_session()
    try:
      files = session.query(Files).filter(Files.id == id).first()
      if not files:
        raise
      return files
    except:
      raise NotFoundError("file not exist").throw()
    finally:
      session.close()

  def verify_file_by_id_name(self, id, name):
    session = self._db.get_session()
    try:
      files = session.query(Files).filter(and_(Files.id == id, Files.custom_name == name)).first()
      if not files:
        raise
      return files
    except:
      raise NotFoundError("file not exist").throw()
    finally:
      session.close()
  
  def get_all_files(self):
    session = self._db.get_session()
    try:
      files = session.query(Files).all()
      return files
    except Exception as e:
      session.rollback()
      raise NotFoundError("error while get files").throw()
    finally:
      session.close()
