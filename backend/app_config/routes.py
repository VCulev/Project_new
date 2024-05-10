from backend.authentification.functionality import (validate_schema_login_route, validate_schema_registration_route)
from backend.utils.raise_utils import json_response
from backend.utils.auth_hash import generate_user_id
from backend.utils.token_utils import generate_auth_user_pack
from backend.mongodb import mongo_utils as mongodb
from backend.redisdb import redis_utils as redis_db


async def add_response_headers(_, response):
    response.headers["Accept"] = "application/json"


async def handle_route(request):
    headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }

    if request.method == "OPTIONS":
        return json_response(200, description="[OK]", headers=headers)


async def register_route(request):
    user_data: dict = request.json

    if not validate_schema_registration_route(user_data):
        return json_response(400, description=f"Provided fields are not valid.")

    sanic_ref = request.route.ctx.refsanic.ctx
    user_id, user_data = generate_user_id(user_data, get_user=True)

    user_role = "admin"

    user_signature = {
        "email": user_data.get("email"),
        "login": user_data.get("login")
    }

    user_exist = await mongodb.exists_user(sanic_ref.mongo, user_signature)
    if user_exist:
        return json_response(401, description=f"Email address or login is being used by another user.")

    user_data["role"] = user_role

    await mongodb.register_user(sanic_ref.mongo, user_data)

    return json_response(200, description=f"Registered successfully.")


async def login_user(request):
    user_data: dict = request.json
    if not validate_schema_login_route(user_data):
        return json_response(400, description='Provided fields are not valid')

    sanic_ref = request.route.ctx.refsanic.ctx
    user_id = generate_user_id(user_data)
    user_signature = {"id": user_id}

    user_exists = await mongodb.exists_user(sanic_ref.mongo, user_signature)
    if not user_exists:
        return json_response(401, description=f"User was not found")

    token, session_id = generate_auth_user_pack()
    await redis_db.remember_user_session(sanic_ref.redis, token, user_id, session_id)
    return json_response(200, token=token, session_id=session_id, user_id=user_id,
                         description=f'User was successfully logged in')
