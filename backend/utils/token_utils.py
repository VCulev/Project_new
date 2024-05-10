from secrets import token_hex


def generate_auth_user_pack(session_length=10, token_length=10):
    return token_hex(token_length), token_hex(session_length)
