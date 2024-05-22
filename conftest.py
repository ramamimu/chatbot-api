import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.services.postgres.models import Base
from config import DB_URI_TEST

# Define a fixture for the test database
@pytest.fixture(scope='module')
def test_engine():
    # Use the actual database URI for testing
    engine = create_engine(DB_URI_TEST)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture(scope='module')
def test_session_factory(test_engine):
    """Returns a SQLAlchemy session factory bound to the test engine."""
    Session = scoped_session(sessionmaker(bind=test_engine))
    yield Session
    Session.remove()

@pytest.fixture(scope='function')
def db_session(test_session_factory):
    """Provides a transactional scope around a series of operations."""
    session = test_session_factory()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
