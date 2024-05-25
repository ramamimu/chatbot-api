import os
import aiofiles
import shutil

from config import DOCUMENT_PATH

class FileStorageService:
  _relative_path = DOCUMENT_PATH

  def __init__(self) -> None:
    pass

  async def save_file_to_folder(self, title, file):
    # If ".pdf" is found, remove it
    if title.endswith(".pdf"):
        folder_name = title[:-4]
    else:
        folder_name = title
    
    full_path = os.path.join(self._relative_path, folder_name)
    # check is path already exist
    if not os.path.exists(full_path):
      # create folder
      os.makedirs(full_path)
    else:
      print("Folder already exist")
      raise FileExistsError(f"Folder '{full_path}' already exists")

    # save file in the folder
    file_path = os.path.join(full_path, file.filename)
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(await file.read())
    
    return full_path
  
  def delete_directory(self, full_path):
    # Check if the directory exists
    if os.path.exists(full_path) and os.path.isdir(full_path):
        # Remove the directory and its contents
        shutil.rmtree(full_path)
    else:
        raise FileNotFoundError(f"Folder '{full_path}' does not exist") 