from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from src.services.postgres.models import Base

class Files(Base):
  __tablename__ = "files"

  id = Column(Integer, primary_key=True, autoincrement=True)
  custom_name = Column(String(200), unique=True, nullable=False)
  file_name = Column(String(200), unique=False, nullable=False)
  path = Column(String(200), unique=True, nullable=False)
  created = Column(DateTime, default=func.now())
  last_modified = Column(DateTime, default=func.now(), onupdate=func.now())

  def __repr__(self):
    return f"id: {self.id}, name: {self.custom_name}, file name: {self.file_name}, path: {self.path}"