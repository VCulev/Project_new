def validate_schema_login_route(schema) -> bool:
    field_login = schema.get("login")
    field_password = schema.get("password")
    if schema.__len__() != 2 \
            or not isinstance(field_login, str) \
            or not isinstance(field_password, str):
        return False
    return True


def validate_schema_registration_route(schema) -> bool:
    field_login = schema.get("login")
    field_password = schema.get("password")
    field_email = schema.get("email")
    if schema.__len__() != 3 \
            or not isinstance(field_login, str) \
            or not isinstance(field_password, str) \
            or not isinstance(field_email, str):
        return False
    return True
