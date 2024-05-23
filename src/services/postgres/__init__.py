from threading import Lock
import sqlalchemy
from sqlalchemy.orm import (
  sessionmaker
)
from config import DB_URI


# reference code: https://github.com/ArjanCodes/examples/blob/main/2024/sqlalchemy/relationship.py
class PostgresDb:
  """
  As Singleton Class
  
  Usage example:
  postgres_db = PostgresDb()

  def insert_data(session):
      new_file = Files(name="example.txt", path="/path/to/example.txt")
      session.add(new_file)

  postgres_db.transaction(insert_data)
  """

  _instance = None
  _lock = Lock()

  def __new__(cls, *args, **kwargs):
      with cls._lock:
          if cls._instance is None:
              cls._instance = super().__new__(cls)
              cls._instance._initialized = False
      return cls._instance

  def __init__(self, db_uri=""):
      if self._initialized:
          return

      print("Arguments passed to __init__ DB: ", db_uri)

      if db_uri == "":
          db_uri = DB_URI
      
      self._db = sqlalchemy.create_engine(db_uri)
      self._session = sessionmaker(bind=self._db)
      self._initialized = True

  def transaction(self, fn):
    session = self._session()
    try:
      fn(session)
      session.commit()
    except Exception as e:
      session.rollback()
      print(f"Error transaction: {e}")
      raise
    finally:
      session.close()

