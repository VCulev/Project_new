async def remember_user_session(redis_db, token, user_id, session_id, expire_in_seconds=900):
    await redis_db.setex(user_id, expire_in_seconds, f"{session_id},{token}")


async def check_user_token(redis_db, token, user_id, session_id) -> bool:
    response = await redis_db.get(user_id)
    return session_id in response and token in response
