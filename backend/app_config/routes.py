import requests
from bs4 import BeautifulSoup
from sanic import response
from backend.authentification.functionality import (
    validate_schema_login_route,
    validate_schema_registration_route
)
from backend.utils.raise_utils import json_response
from backend.utils.auth_hash import generate_user_id
from backend.utils.token_utils import generate_auth_user_pack
from backend.mongodb import mongo_utils as mongodb
from backend.redisdb import redis_utils as redis_db

OPEN_TRIVIA_API_BASE_URL = "https://opentdb.com/api.php"


async def add_response_headers(_, responses):
    """Add headers to responses."""
    responses.headers["Accept"] = "application/json"


async def handle_options_route(request):
    """Handle OPTIONS request."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    if request.method == "OPTIONS":
        return json_response(200, description="[OK]", headers=headers)


async def register_user(request):
    """Handle user registration."""
    user_data = request.json

    if not validate_schema_registration_route(user_data):
        return json_response(400, description="Provided fields are not valid.")

    sanic_ref = request.route.ctx.refsanic.ctx
    user_id, user_data = generate_user_id(user_data, get_user=True)
    user_role = "admin"

    user_signature = {
        "email": user_data.get("email"),
        "login": user_data.get("login")
    }

    user_exists = await mongodb.exists_user(sanic_ref.mongo, user_signature)
    if user_exists:
        return json_response(401, description="Email address or login is already used by another user.")

    user_data["role"] = user_role
    await mongodb.register_user(sanic_ref.mongo, user_data)

    return json_response(200, description="Registered successfully.")


async def login_user(request):
    """Handle user login."""
    user_data = request.json

    if not validate_schema_login_route(user_data):
        return json_response(400, description="Provided fields are not valid.")

    sanic_ref = request.route.ctx.refsanic.ctx
    user_id = generate_user_id(user_data)
    user_signature = {"id": user_id}

    user_exists = await mongodb.exists_user(sanic_ref.mongo, user_signature)
    if not user_exists:
        return json_response(401, description="User not found.")

    token, session_id = generate_auth_user_pack()
    await redis_db.remember_user_session(sanic_ref.redis, token, user_id, session_id)
    return json_response(200, token=token, session_id=session_id, user_id=user_id,
                         description="User successfully logged in.")


async def get_quiz(request):
    """Fetch a programming quiz."""
    params = {
        "amount": 10,
        "type": "multiple",
        "difficulty": "medium",
        "encode": "url3986",
        "category": 18
    }

    response_from_api = requests.get(OPEN_TRIVIA_API_BASE_URL, params=params)

    if response_from_api.ok:
        quiz_data = response_from_api.json()
        return response.json(quiz_data)
    else:
        return json_response(500, description="Can't generate quiz.")


def scrape_stackoverflow():
    """Scrape Stack Overflow for recent questions."""
    url = 'https://stackoverflow.com/questions'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        questions = soup.find_all('div', class_='s-post-summary')
        results = []

        for question in questions:
            title = question.find('a', class_='s-link').text.strip()
            link = question.find('a', class_='s-link')['href']
            results.append({'title': title, 'link': f"https://stackoverflow.com{link}"})

        return results
    else:
        return []


async def scrape_questions(request):
    """Handle request to scrape Stack Overflow questions."""
    questions = scrape_stackoverflow()
    return response.json(questions)


async def logout_user(request):
    """Handle user logout."""
    token = request.headers.get("Authorization")
    if not token:
        return json_response(401, description="Authorization token not provided.")

    sanic_ref = request.route.ctx.refsanic.ctx
    await redis_db.forget_user_session(sanic_ref.redis, token)
    return json_response(200, description="User successfully logged out.")