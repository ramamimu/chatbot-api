import pytest
from unittest.mock import patch, Mock, AsyncMock

from src.services.storage.files_storage_service import FileStorageService


@pytest.mark.asyncio
@patch('os.makedirs')
@patch('os.path.exists')
async def test_save_file_to_folder_when_not_exist(mock_exists, mock_makedirs):
  # Arrange
  service = FileStorageService()
  title = "example_document.pdf"
  expected_path = "src/commons/documents/example_document"
  
  # Set up the mock behavior
  mock_exists.return_value = False
  mock_file = Mock()
  mock_file.filename = "example_document.pdf"
  mock_file.read = AsyncMock(return_value=b"Test content")

  # Patch aiofiles.open separately
  with patch('aiofiles.open') as mock_aioopen:
      # Act
      await service.save_file_to_folder(title, mock_file)
      
      # Assert
      mock_exists.assert_called_once_with(expected_path)
      mock_makedirs.assert_called_once_with(expected_path)
      mock_aioopen.assert_called_once_with(expected_path + '/' + mock_file.filename, 'wb')
      mock_aioopen.return_value.__aenter__.return_value.write.awaited_once_with(b"Test content")

@pytest.mark.asyncio
@patch('os.makedirs')
@patch('os.path.exists')
async def test_save_file_to_folder_when_exist(mock_exists, mock_makedirs):
  # Arrange
  service = FileStorageService()
  title = "example_document.pdf"
  expected_path = "src/commons/documents/example_document"

  # Set up the mock behavior
  mock_exists.return_value = True
  mock_file = Mock()

  # Assert
  with pytest.raises(FileExistsError) as excinfo:
    await service.save_file_to_folder(title, mock_file)

  assert str(excinfo.value) == f"Folder '{expected_path}' already exists"
  mock_exists.assert_called_once_with(expected_path)
  mock_makedirs.assert_not_called()
  mock_file.save.assert_not_called()
