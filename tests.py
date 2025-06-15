import pytest
from fastapi.testclient import TestClient
from main import app  # Adjust if your app is in a different file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
  Base.metadata.create_all(bind=engine)
  yield
  Base.metadata.drop_all(bind=engine)


def test_submit_usage_event():
  response = client.post("/api/v1/usage/", json={
    "user_id": 1,
    "usage_type": "cpu",
    "usage_amount": 10,
    "usage_unit": "percentage"
  })
  assert response.status_code == 200
  data = response.json()
  assert data["user_id"] == 1
  assert data["usage_type"] == "cpu"


def test_get_usage_events():
  response = client.get("/api/v1/usage/1")
  assert response.status_code == 200
  data = response.json()
  assert isinstance(data, list)


def test_get_usage_events_not_found():
  response = client.get("/api/v1/usage/999")
  assert response.status_code == 404


def test_process_report():
  response = client.post("api/v1/reports/1")
  assert response.status_code == 200
  assert "Job_id" in response.json()
