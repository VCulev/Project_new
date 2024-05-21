from bs4 import BeautifulSoup
from httpx import AsyncClient
from backend.authentification.functionality import (
    validate_schema_login_route,
    validate_schema_registration_route
)
from backend.utils.raise_utils import json_response, j_response
from backend.utils.auth_hash import generate_user_id
from backend.utils.token_utils import generate_auth_user_pack
from backend.mongodb import mongo_utils as mongodb
from backend.redisdb import redis_utils as redis_db
from sanic_ext import openapi


@openapi.summary("Add headers to responses")
async def add_response_headers(_, responses):
    """Add headers to responses."""
    responses.headers["Accept"] = "application/json"


@openapi.summary("Register a new user")
@openapi.body({"application/json": {"example": {"email": "user@example.com", "login": "user123", "password": "pass"}}})
@openapi.response(200, {"application/json": {"example": {"description": "Registered successfully."}}})
@openapi.response(400, {"application/json": {"example": {"description": "Provided fields are not valid."}}})
@openapi.response(401, {"application/json": {"example": {"description": "Email address or login is already used by another user."}}})
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


@openapi.summary("Login a user")
@openapi.body({"application/json": {"example": {"login": "user123", "password": "pass"}}})
@openapi.response(200, {"application/json":
                            {"example": {"description": "User successfully logged in.",
                                         "token": "token", "session_id": "session_id", "user_id": "user_id"}}})
@openapi.response(400, {"application/json": {"example": {"description": "Provided fields are not valid."}}})
@openapi.response(401, {"application/json": {"example": {"description": "User not found."}}})
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


@openapi.summary("Logout a user")
@openapi.parameter("Authorization", str, "header")
@openapi.response(200, {"application/json": {"example": {"description": "User successfully logged out."}}})
@openapi.response(401, {"application/json": {"example": {"description": "Authorization token not provided."}}})
async def logout_user(request):
    """Handle user logout."""
    token = request.headers.get("Authorization")
    if not token:
        return json_response(401, description="Authorization token not provided.")

    sanic_ref = request.route.ctx.refsanic.ctx
    await redis_db.forget_user_session(sanic_ref.redis, token)
    return json_response(200, description="User successfully logged out.")


@openapi.summary("Fetch a programming quiz")
@openapi.response(200, {"application/json": {"example": {"results": [
    {"category": "Science: Computers", "type": "multiple", "difficulty": "medium",
     "question": "What does CPU stand for?", "correct_answer": "Central Processing Unit",
     "incorrect_answers": ["Central Process Unit", "Computer Personal Unit", "Central Processor Unit"]}]}}})
@openapi.response(500, {"application/json": {"example": {"description": "Failed to fetch quiz."}}})
async def get_quiz(request):
    """Fetch a programming quiz."""
    params = {
        "amount": 10,
        "type": "multiple",
        "difficulty": "medium",
        "encode": "url3986",
        "category": 18
    }

    async with AsyncClient() as client:
        response = await client.get(
            "https://opentdb.com/api.php",
            params=params)

        if response.status_code != 200:
            return json_response(500, description="Failed to fetch quiz.")

        data = response.json()
        return j_response(data)


@openapi.summary("Scrape Stack Overflow for recent questions")
@openapi.response(200, {"application/json": {
    "example": [{"title": "How to scrape a website?", "link": "https://stackoverflow.com/questions/1"}]}})
@openapi.response(500, {"application/json": {"example": {"description": "Failed to scrape Stack Overflow."}}})
async def scrape_stackoverflow():
    """Scrape Stack Overflow for recent questions."""
    async with AsyncClient() as client:
        response = await client.get(
            "https://stackoverflow.com/questions"
        )

        if response.status_code != 200:
            return json_response(500, description="Failed to scrape Stack Overflow.")

        soup = BeautifulSoup(response.text, "html.parser")
        questions = soup.find_all('div', class_='s-post-summary')
        results = []

        for question in questions:
            title = question.find('a', class_='s-link').text.strip()
            link = question.find('a', class_='s-link')['href']
            results.append({'title': title, 'link': f"https://stackoverflow.com{link}"})

        return results


@openapi.summary("Scrape Stack Overflow questions")
@openapi.response(200, {"application/json": {
    "example": [{"title": "How to scrape a website?", "link": "https://stackoverflow.com/questions/1"}]}})
async def scrape_questions(request):
    """Handle request to scrape Stack Overflow questions."""
    questions = await scrape_stackoverflow()
    return j_response(questions)


@openapi.summary("Handle OPTIONS request")
@openapi.parameter("Access-Control-Allow-Origin", str, "header")
@openapi.parameter("Access-Control-Allow-Methods", str, "header")
@openapi.parameter("Access-Control-Allow-Headers", str, "header")
@openapi.response(200, {"application/json": {"example": {"description": "[OK]"}}})
async def handle_options_route(request):
    """Handle OPTIONS request."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    if request.method == "OPTIONS":
        return json_response(200, description="[OK]", headers=headers)