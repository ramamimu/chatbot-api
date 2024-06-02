from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.services.postgres.models import Base

class Files(Base):
  __tablename__ = "files"

  id = Column(Integer, primary_key=True, autoincrement=True)
  custom_name = Column(String(100), unique=True, nullable=False)
  file_name = Column(String(100), unique=False, nullable=False)
  path = Column(String(100), unique=True, nullable=False)
  created = Column(DateTime, default=func.now())
  last_modified = Column(DateTime, default=func.now(), onupdate=func.now())

  # Define the relationship to TopicFiles
  topics = relationship("TopicFiles", back_populates="file")

  def __repr__(self):
    return f"id: {self.id}, name: {self.custom_name}, file name: {self.file_name}, path: {self.path}"

class Topics(Base):
  __tablename__ = "topics"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(100), unique=True, nullable=False)

  # Define the relationship to TopicFiles
  files = relationship("TopicFiles", back_populates="topic")

  def __repr__(self):
      return f"id: {self.id}, name: {self.name}"

class TopicFiles(Base):
  __tablename__ = "topic_files"
  id = Column(Integer, primary_key=True, autoincrement=True)
  file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
  topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)

  # Relationships
  file = relationship("Files", back_populates="topics")
  topic = relationship("Topics", back_populates="files")

  def __repr__(self):
      return f"id: {self.id}, file_id: {self.file_id}, topic_id: {self.topic_id}"