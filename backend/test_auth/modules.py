urls = {
    "LOGIN": "/api/login_user",
    "REGISTRATION": "/api/register_user",
}

registration_credentials = {
    "login": "nick",
    "password": "nick123",
    "email": "nick@yahoo.com",
}

login_credential = {
    "login": "nick",
    "password": "nick123"
}


def api_url(path):
    return f"http://0.0.0.0:4000{path}"
