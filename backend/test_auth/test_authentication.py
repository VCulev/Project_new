from backend.test_auth.modules import api_url, urls, login_credential, registration_credentials
import requests


def test_check_registration():
    print(f"Registration: ", end="")
    response = requests.post(
        api_url(urls["REGISTRATION"]),
        json=registration_credentials
    )

    j_response = response.json()
    j_keys = j_response.keys()

    if response.status_code != 200:
        print(f"[BAD]:  {j_response}")

    token = j_response.get("token")
    session_id = j_response.get("session_id")
    user_id = j_response.get("user_id")

    assert response.status_code == 200
    assert len(j_keys) == 1

    print(f"[OK]:  {j_response}")

    return token, session_id, user_id


def test_login():
    print(f"Login: ", end="")
    response = requests.post(
        api_url(urls["LOGIN"]),
        json=login_credential
    )

    j_response = response.json()

    if response.status_code != 200:
        print(f"[BAD]: {j_response}", end="")

    token = j_response["token"]
    session_id = j_response["session_id"]
    user_id = j_response["user_id"]

    assert response.status_code == 200
    assert len(j_response.keys()) == 4
    for k, v in j_response.items():
        assert isinstance(v, str)
        assert len(v) > 0

    print(f"[OK]: {j_response}")

    return token, session_id, user_id


def run_tests():
    test_check_registration()
    test_login()


if __name__ == "__main__":
    run_tests()




