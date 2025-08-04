import io
import time

import pytest
import requests

BASE_URL = "http://localhost:5000/api"


@pytest.fixture(scope="module")
def registered_user():
    unique_email = f"test_user_{int(time.time())}@example.com"
    password = "test_password"
    data = {"email": unique_email, "password": password}
    response = requests.post(f"{BASE_URL}/register", data=data)
    print(f"Register response status: {response.status_code}, text: {response.text}")  # Added print
    assert response.status_code == 201
    return {"email": unique_email, "password": password}


@pytest.fixture(scope="module")
def logged_in_session(registered_user):
    session = requests.Session()
    data = {"email": registered_user["email"], "password": registered_user["password"]}
    response = session.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    # Verify session is authenticated
    verify_response = session.get(f"{BASE_URL}/user")
    assert verify_response.status_code == 200, f"Session not authenticated after login: {verify_response.text}"
    return session


def test_login_user(registered_user):
    data = {"email": registered_user["email"], "password": registered_user["password"]}
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 200
    assert response.json() == {"result": "OK"}


def test_get_user(logged_in_session):
    response = logged_in_session.get(f"{BASE_URL}/user")
    assert response.status_code == 200
    assert "email" in response.json()


def test_logout_user(logged_in_session):
    response = logged_in_session.post(f"{BASE_URL}/logout")
    assert response.status_code == 200
    # After logout, trying to access a protected endpoint should fail
    response = logged_in_session.get(f"{BASE_URL}/user")
    assert response.status_code == 401


def test_upload_profile_picture(registered_user):
    session = requests.Session()
    login_data = {"email": registered_user["email"], "password": registered_user["password"]}
    login_response = session.post(f"{BASE_URL}/login", json=login_data)
    assert login_response.status_code == 200, f"Login failed in upload test: {login_response.text}"

    file_content = b"dummy image content"
    files = {"profile_picture": ("profile.png", io.BytesIO(file_content), "image/png")}
    response = session.post(f"{BASE_URL}/profile/picture", files=files)
    assert response.status_code == 200, f"Upload profile picture failed: {response.text}"


def test_get_profile_picture(registered_user):
    session = requests.Session()
    login_data = {"email": registered_user["email"], "password": registered_user["password"]}
    login_response = session.post(f"{BASE_URL}/login", json=login_data)
    assert login_response.status_code == 200, f"Login failed in get profile picture test: {login_response.text}"

    # First, upload a picture to ensure it exists
    file_content = b"dummy image content for get"
    files = {"profile_picture": ("profile_to_get.png", io.BytesIO(file_content), "image/png")}
    response = session.post(f"{BASE_URL}/profile/picture", files=files)
    assert response.status_code == 200, f"Upload for get profile picture failed: {response.text}"
    profile_picture_path = response.json()["profile_picture"]

    # Extract user_email and filename from the path
    parts = profile_picture_path.split("/")
    user_email = parts[-2]
    filename = parts[-1]

    response = requests.get(f"{BASE_URL}/profile/pictures/{user_email}/{filename}")
    assert response.status_code == 200
    assert response.content == file_content
