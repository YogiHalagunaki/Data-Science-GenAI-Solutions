# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
# from app.views import app  # ensure the app is imported
# client = TestClient(app)

import requests 

def test_schema_endpoint():
    response = requests.get("/Text_to_SQL/schema")
    #response = client.get("/Text_to_SQL/schema")
    assert response.status_code == 200
    assert "schema" in response.json()

def test_query_endpoint_count():
    response = requests.post("/Text_to_SQL/query", json={"question": "How many rows are there?"})
    #response = client.post("/Text_to_SQL/query", json={"question": "How many rows are there?"})
    assert response.status_code in (200, 400)  # might fail gracefully if no data
    data = response.json()
    assert "status" in data

def test_query_endpoint_list():
    response = requests.post("/Text_to_SQL/query", json={"question": "List all records"})
    #response = client.post("/Text_to_SQL/query", json={"question": "List all records"})
    assert response.status_code in (200, 400)
    data = response.json()
    assert "status" in data
