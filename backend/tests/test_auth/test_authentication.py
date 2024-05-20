from backend.tests.modules.modules import api_url, urls, login_credential, registration_credentials
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient() as client:
        print(f"[REGISTRATION]: ", end="")
        response = await client.post(
            api_url(urls["REGISTRATION"]),
            json=registration_credentials
        )

        j_response = response.json()
        j_keys = j_response.keys()

        if response.status_code != 200:
            print(f"[BAD]: {j_response}", end="")

        token = j_response.get("token")
        session_id = j_response.get("session_id")
        user_id = j_response.get("user_id")

        assert response.status_code == 200
        assert len(j_keys) == 1

        print(f"[OK]: {j_response}")

        return token, session_id, user_id


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient() as client:
        print(f"[LOGIN]: ", end="")

        response = await client.post(
            api_url(urls["LOGIN"]),
            json=login_credential
        )

        j_response = response.json()

        token = j_response.get("token")
        session_id = j_response.get("session_id")
        user_id = j_response.get("user_id")

        if response.status_code != 200:
            print(f"[BAD]: {j_response}", end="")

        assert response.status_code == 200
        assert len(j_response.keys()) == 4
        for k, v in j_response.items():
            assert isinstance(v, str)
            assert len(v) > 0

        print(f"[OK]: {j_response}")
        return token, session_id, user_id


@pytest.mark.asyncio
async def test_logout_user():
    token, _, _ = await test_login_user()

    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        print(f"[LOGOUT]: ", end="")
        response = await client.post(
            api_url(urls["LOGOUT"]),
            headers=headers
        )

        j_response = response.json()

        if response.status_code != 200:
            print(f"[BAD]: {j_response}", end="")

        assert response.status_code == 200
        print(f"[OK]: {j_response}")
        return token
