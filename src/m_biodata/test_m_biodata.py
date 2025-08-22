import logging
from fastapi.testclient import TestClient
import pytest

from src import app

log = logging.getLogger(__name__)
client = TestClient(app)

id = "1755677180"
def test_find_by_id_success():
    response = client.get("/api/v1/m-biodata/" + id, headers={"Content-Type": "application/json"})
    assert response.status_code == 200

def test_find_list_success():
    response = client.get("/api/v1/m-biodata/" + id, headers={"Content-Type": "application/json"})
    assert response.status_code == 200

