urls = {
    "LOGIN": "/api/login_user",
    "REGISTRATION": "/api/register_user",
    "LOGOUT": "/api/logout_user",
    "QUIZ": "/api/quiz",
    "SCRAPING": "/api/scrape-newsletter",
}

registration_credentials = {
    "login": "mar",
    "password": "1111",
    "email": "mar@yahoo.com",
}

login_credential = {
    "login": "mar",
    "password": "1111"
}


def api_url(path):
    return f"http://0.0.0.0:4000{path}"
