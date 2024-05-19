async def remember_user_session(redis_db, token, user_id, session_id, expire_in_seconds=900):
    await redis_db.setex(user_id, expire_in_seconds, f"{session_id},{token}")


async def forget_user_session(redis_db, token):
    user_session = await redis_db.get(token)
    if user_session:
        user_id, _ = user_session.decode().split(',')
        await redis_db.delete(user_id)
        await redis_db.delete(token)