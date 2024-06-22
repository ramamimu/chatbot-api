from src.exceptions.invariant_error import InvariantError
from src.commons.types.files_db_type import FilesEntity

class FileUtils:
  def __init__(self) -> None:
    pass

  @staticmethod
  def validate_filename(filename: str):
    if "preprocessing-" in filename:
      raise InvariantError("filename contains 'preprocessing-'").throw()
    if ".pdf" not in filename:
      raise InvariantError("file format must be .pdf").throw()
  
  @staticmethod
  def files_db_entity(files):
    files_entity = [ 
      FilesEntity(
        id=file.id,
        name=file.custom_name,
        filename=file.file_name,
        created=file.created,
        lastModified=file.last_modified
      )
      for file in files]
    return files_entity