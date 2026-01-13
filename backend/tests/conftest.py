import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db(db_engine):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db):
    """Provide test client with mocked Celery to avoid Redis dependency."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    # Mock Celery tasks to avoid Redis connection errors in test environment
    with patch("app.core.celery.celery_app") as mock_celery:
        # Make the celery_app and its tasks behave like real Celery mocks
        mock_task = MagicMock()
        mock_task.delay = MagicMock(return_value=MagicMock(id="test-task-id"))
        mock_celery.task = MagicMock(return_value=lambda f: mock_task)

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
