from typing import Type
from src.exceptions.invariant_error import InvariantError
from src.exceptions.not_found_error import NotFoundError
from src.services.postgres import PostgresDb
from src.services.postgres.models.tables import Topics


class TopicsDbService():
  def __init__(self, db) -> None:
    self._db: Type[PostgresDb] = db

  def add_topic(self, topic_name):
    new_topic = Topics(name=topic_name)
    self._db.transaction(lambda session: session.add(new_topic))
    # to make sure the transaction already set 
    return new_topic
  
  def update_topic_by_id(self, topic_id, topic_name):
    session = self._db.get_session()
    try:
      topic = session.query(Topics).filter_by(id=topic_id).first()
      if topic:
        topic.name = topic_name
        session.commit()
        session.refresh(topic)
      else:
        raise 
    except:
      raise NotFoundError("topic not found").throw()
    finally:
      session.close()

  def verify_availability_topic_name(self, topic_name):
    session = self._db.get_session()
    try:
      topics = session.query(Topics).filter(Topics.name == topic_name).first()
      
      # if exist, throw error
      if topics:
        raise 
    except Exception as e:
      print(e)
      raise InvariantError("topic name already exist").throw()
    finally:
      session.close()
  
  def verify_existance_topic_by_id(self, topic_id):
    session = self._db.get_session()
    try:
      topics = session.query(Topics).filter(Topics.id == topic_id).first()
      
      # if exist, throw error
      if not topics:
        raise
    except:
      raise InvariantError("topic is not exist").throw()
    finally:
      session.close()

  def get_topic_by_id(self, topic_id):
    session = self._db.get_session()
    try:
      topics = session.query(Topics).filter(Topics.id == topic_id).first()
      return topics
    except:
        raise InvariantError("topic not found").throw()
    finally:
      session.close()

  def get_topics(self):
    session = self._db.get_session()
    try:
      topics = session.query(Topics).all()
      return topics
    finally:
      session.close()
  
  def delete_topic_by_id(self, topic_id):
    self._db.transaction(lambda session: session.query(Topics).filter(Topics.id == topic_id).delete())
  

