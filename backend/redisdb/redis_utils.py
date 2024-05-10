async def remember_user_session(redis_db, token, user_id, session_id, expire_in_seconds=900):
    await redis_db.setex(user_id, expire_in_seconds, f"{session_id},{token}")


async def check_user_token(redis_db, user_id, session_id, token):
    response = await redis_db.get(user_id)
    if response:
        session_token_pair = response.decode().split(',')
        stored_session_id = session_token_pair[0]
        stored_token = session_token_pair[1]
        return session_id == stored_session_id and token == stored_token
    else:
        return False
