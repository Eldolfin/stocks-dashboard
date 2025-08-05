import time
import anyio
import pytest
import requests
from functools import partial

BASE_URL = "http://localhost:5000/api"
NUM_USERS = 50


async def register_and_login_user(user_id, results):
    """Register a user and then log in."""
    email = f"testuser_async_{user_id}_{int(time.time() * 1000000)}@test.com"
    password = "password123"
    register_payload = {"email": email, "password": password}
    login_payload = {"email": email, "password": password}

    try:
        register_func = partial(requests.post, f"{BASE_URL}/register", data=register_payload)
        register_response = await anyio.to_thread.run_sync(register_func)
        results[user_id] = {"register_status": register_response.status_code}

        if register_response.status_code == 201:
            login_func = partial(requests.post, f"{BASE_URL}/login", json=login_payload)
            login_response = await anyio.to_thread.run_sync(login_func)
            results[user_id]["login_status"] = login_response.status_code
        else:
            results[user_id]["login_status"] = register_response.text

    except requests.exceptions.RequestException as e:
        results[user_id] = {"register_status": str(e), "login_status": None}


@pytest.mark.anyio(backend='asyncio')
async def test_concurrent_register_and_login():
    """Test concurrent user registration and login using asyncio."""
    results = {}
    async with anyio.create_task_group() as tg:
        for i in range(NUM_USERS):
            tg.start_soon(register_and_login_user, i, results)

    for i in range(NUM_USERS):
        assert results[i].get("register_status") == 201, f"User {i} failed to register: {results[i]}"
        assert results[i].get("login_status") == 200, f"User {i} failed to log in: {results[i]}"
