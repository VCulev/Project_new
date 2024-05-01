from backend.utils.token_utils import generate_auth_user_token


def validate_schema_login_route(schema) -> bool:
    field_login = schema['login']
    field_password = schema['password']
    if schema.__len__() != 2 \
            or not isinstance(field_login, str) \
            or not isinstance(field_password, str):
        return False
    return True


def validate_schema_register_route(schema) -> bool:
    field_login = schema['login']
    field_password = schema['password']
    field_email = schema['email']
    if schema.__len__() != 3 \
            or not isinstance(field_login, str)\
            or not isinstance(field_password, str)\
            or not isinstance(field_email, str):
        return False
    return True


def validate_schema_patch_user(schema) -> bool:
    field_user_id = schema['user_id']
    field_token = schema['token']
    field_session_id = schema['session_id']
    field_settings = schema['settings']
    if schema.__len__() != 4 \
            or not isinstance(field_user_id, str)\
            or not isinstance(field_token, str)\
            or not isinstance(field_session_id, str)\
            or not isinstance(field_settings, dict):
        return False
    return True


def compose_permission_request(user_data: dict, app_or_prod_id=None, system=False, user_settings=None) -> dict:
    return {
        "target": app_or_prod_id,
        "user_settings": user_settings,
        "user_id": user_data['id'],
        "system": system,
    }



async def update_user_token(user_id, session_id, redis_db):
    new_token = generate_auth_user_token()
    await redis_db.set(user_id, f"{session_id}:{new_token}")
    return new_token