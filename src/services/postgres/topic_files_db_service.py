from typing import List, Type
from sqlalchemy.orm import Session

from src.services.postgres import PostgresDb
from src.services.postgres.models.tables import Files, TopicFiles, Topics

class TopicFilesDbService:
  def __init__(self, db) -> None:
    self._db: Type[PostgresDb] = db

  def add_files_topic(self, topic: Type[Topics], files: List[Type[Files]], is_edit=False):
    def fn(session):
      if not is_edit:
        session.add(topic)
        session.flush() 
      for file in files:
            # Ensure each file is managed by the session, if not already
            if not session.object_session(file):
                session.add(file)
                session.flush()  # Ensure file ID is generated if this is a new file

            association = TopicFiles(file_id=file.id, topic_id=topic.id)
            session.add(association)

    self._db.transaction(fn)
   
  def get_files_by_topic(self, topic_id: str) -> List[Type[Files]]:
      session: Session = self._db.get_session()
      try:
          # Query the TopicFiles association table to get all file_ids for the topic
          associations = session.query(TopicFiles).filter(TopicFiles.topic_id == topic_id).all()
          # Extract file_ids from the associations
          file_ids = [association.file_id for association in associations]
          # Query the Files table to get all files by the collected file_ids
          files = session.query(Files).filter(Files.id.in_(file_ids)).all()
          return files
      finally:
          session.close()
  
  def delete_topic_files_by_topic_id(self, topic_id):
    self._db.transaction(lambda session: session.query(TopicFiles).filter(TopicFiles.topic_id == topic_id).delete())

  def update_files_by_topic_id(self, topic_id, files):
    session = self._db.get_session()
    try:
      session.query(TopicFiles).filter_by(topic_id=topic_id).delete()
    finally:
      session.close()
