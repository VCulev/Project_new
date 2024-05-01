from secrets import token_hex


def generate_auth_user_pack(session_length=10, token_length=10):
    return token_hex(session_length), token_hex(token_length)


def generate_auth_user_token(token_length=10):
    return token_hex(token_length)