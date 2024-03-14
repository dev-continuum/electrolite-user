from fastapi.testclient import TestClient
from app import app
from config import Settings


client = TestClient(app)


def test_search_longitude():
    response = client.get("/stations")
    print(response.json())
    # assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}

