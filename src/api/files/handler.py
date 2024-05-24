from fastapi import File, UploadFile, Form

from src.commons.types.files_api_handler_type import PutEmbedFilesType

class FilesHandler:
  def __init__(self, file_storage_service, files_db_service, embedding_service, vectorstore_service):
    self._file_storage_service = file_storage_service
    self._files_db_service = files_db_service
    self._embedding_service = embedding_service
    self._vectorstore_service = vectorstore_service

  async def put_embed_files_handler(self, name: str = Form(...), file: UploadFile = File(...)):
    """
    1. create dir src/commons/<title> and return the path
    
    2. save file in src/commons/<title>/<title.pdf>
    
    3. write name and path in database
    
    4. split document
    
    5. embed document
    
    6. save embedded document in local
    
    7. update vectorstore
    
    8. update chain (tested does chain still need to update)
    """
    
    full_path:str = await self._file_storage_service.save_file_to_folder(name, file)
    self._files_db_service.add_file(name, file.filename, full_path)
    splitted_document = self._embedding_service.split_document(f"{full_path}/{file.filename}")
    embedded_document = self._embedding_service.embed_document(splitted_document)
    self._embedding_service.save_local_embedded_document(embedded_document, full_path)
    self._vectorstore_service.add_vectostore(full_path)
    
    return {"status":"success"}