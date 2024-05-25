from src.commons.types.files_db_type import FilesEntity

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