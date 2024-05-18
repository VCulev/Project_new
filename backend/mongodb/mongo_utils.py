async def exists_user(mongo_db, search) -> bool:
    result = await mongo_db["quiz"].find_one(search, {"id": 1})
    return result is not None


async def register_user(mongo_db, user_data) -> None:
    await mongo_db["quiz"].insert_one({
        "login": user_data.get("login"),
        "password": user_data.get("password"),
        "email": user_data.get("email"),
        "id": user_data.get("id")
    })
