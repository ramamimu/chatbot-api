from src.services.postgres.models.tables import Files
from src.services.postgres import PostgresDb
from config import DB_URI_TEST

def test_insert_file(db_session):
    postgres_db = PostgresDb(db_uri=DB_URI_TEST)

    new_file_data = {
        'custom_name': 'a test file',
        'file_name': 'test.txt',
        'path': '/path/to/test.txt'
    }

    def insert_data(session):
        new_file = Files(**new_file_data)
        session.add(new_file)

    # Use the transaction method from the singleton to insert data
    postgres_db.transaction(insert_data)

    # Verify the file was inserted
    result = db_session.query(Files).filter_by(custom_name="a test file").one_or_none()
    assert result is not None
    assert result.file_name == "test.txt"
    assert result.custom_name == "a test file"
    assert result.path == "/path/to/test.txt"