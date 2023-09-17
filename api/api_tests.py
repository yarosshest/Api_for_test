from fastapi.testclient import TestClient
from database.async_db import asyncHandler as DB
import asyncio
from .api import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}


def test_register():
    test = {
        "log": "Test_log",
        "password": "Test_password",
    }

    response = client.get("/register", params=test)
    assert response.status_code == 200

    asyncio.run(DB.dell_user("Test_log", "Test_password"))


def test_err_register():
    test = {
        "log": "Test_log",
        "password": "Test_password",
    }

    client.get("/register", params=test)
    response = client.get("/register", params=test)
    assert response.status_code == 405

    asyncio.run(DB.dell_user("Test_log", "Test_password"))


def test_login():

    client.get("/register", params={"log": "Test_log", "password": "Test_password"})
    response = client.get("/login", params={"log": "Test_log", "password": "Test_password"})
    assert response.status_code == 200

    asyncio.run(DB.dell_user("Test_log", "Test_password"))


def test_err_login():
    response = client.get("/login", params={"log": "Test_log", "password": "Test_password"})
    assert response.status_code == 404

    assert response.json() == {"message": "User not found"}
