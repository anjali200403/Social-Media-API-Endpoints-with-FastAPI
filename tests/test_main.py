from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_root():
    res=client.options("/")
    assert res.json().get("message")=="system is up and running"