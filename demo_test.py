
# Run with `pytest ./demo_test.py`

from fastapi.testclient import TestClient

from demo import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
