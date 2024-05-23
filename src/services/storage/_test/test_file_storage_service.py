import os
import pytest
import asyncio
from unittest import mock
from aiofiles import open as aioopen
from src.services.storage.files_storage_service import FileStorageService

@pytest.fixture
def file_storage_service():
    return FileStorageService()

@pytest.fixture
def mock_file():
    file = mock.Mock()
    file.filename = 'test_file.txt'
    file.read = mock.AsyncMock(return_value=b"Test content")
    return file

@pytest.fixture
def tmp_path():
    path = "../commons/documents/test_folder"
    yield path
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)

@pytest.mark.asyncio
async def test_save_file_to_folder(file_storage_service, mock_file, tmp_path):
    # Ensure the directory does not exist before the test
    if os.path.exists(tmp_path):
        os.rmdir(tmp_path)
    
    title = "test_folder.pdf"
    full_path = await file_storage_service.save_file_to_folder(title, mock_file)
    
    # Check that the directory was created
    assert os.path.exists(tmp_path)
    
    # Check that the file was saved correctly
    file_path = os.path.join(tmp_path, mock_file.filename)
    assert os.path.exists(file_path)
    
    # Read the file and check its content
    async with aioopen(file_path, 'rb') as f:
        content = await f.read()
        assert content == b"Test content"

@pytest.mark.asyncio
async def test_save_file_to_folder_no_pdf_extension(file_storage_service, mock_file, tmp_path):
    title = "test_folder"
    full_path = await file_storage_service.save_file_to_folder(title, mock_file)
    
    # Check that the directory was created
    assert os.path.exists(tmp_path)
    
    # Check that the file was saved correctly
    file_path = os.path.join(tmp_path, mock_file.filename)
    assert os.path.exists(file_path)
    
    # Read the file and check its content
    async with aioopen(file_path, 'rb') as f:
        content = await f.read()
        assert content == b"Test content"

@pytest.mark.asyncio
async def test_save_file_to_existing_folder(file_storage_service, mock_file, tmp_path):
    # Create the folder before running the test
    os.makedirs(tmp_path)
    
    title = "test_folder"
    with pytest.raises(FileExistsError):
        await file_storage_service.save_file_to_folder(title, mock_file)
