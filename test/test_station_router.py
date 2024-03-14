from fastapi.testclient import TestClient
from app.station_routers import station_router
from main import app


client = TestClient(app)

def test_read_main():
    response = client.get("/book/charger")
    print(response)
    # assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}

