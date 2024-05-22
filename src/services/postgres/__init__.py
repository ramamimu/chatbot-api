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
              db_uri = DB_URI
              # for testing purpose
              if kwargs['db_uri'] != None:
                 db_uri = kwargs['db_uri']
              cls._instance._db = sqlalchemy.create_engine(db_uri)
              cls._instance._session = sessionmaker(bind=cls._instance._db)
      return cls._instance
  
  def change_connection(self, DB_URI):
    self._instance._db = sqlalchemy.create_engine(DB_URI)
    self._instance._session = sessionmaker(bind=self._instance._db)


  def transaction(self, fn):
    session = self._session()
    try:
      fn(session)
      session.commit()
      print("Data transaction successfully")
    except Exception as e:
      session.rollback()
      print(f"Error transaction: {e}")
      raise
    finally:
      session.close()

