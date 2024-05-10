from pymongo.errors import CollectionInvalid
from motor.motor_asyncio import AsyncIOMotorClient
from rapidjson import dumps
import redis.asyncio as redis


DATABASE_NAME = "COURSE_GENERATOR"

COLLECTIONS = ["courses"]

INDEXES = {
    "courses": [
        ('id', dict(unique=True, name='user_id')),
        ('name', dict(name='user_name')),
        ('login', dict(name='login_1')),
        ('email', dict(name='email_1')),
        ('password', dict(name='password_1'))
    ]
}


def create_database(db_conn, db_name):
    print(f"COURSE GENERATOR [STARTUP]: create database {db_name}")
    _ = db_conn[db_name]
    db_conn.get_database(db_name)


async def create_collections(db_conn, db_name, collections):
    for col_name in collections:
        try:
            await db_conn[db_name].create_collection(col_name)
            print(f"COURSE GENERATOR [STARTUP]: collection {col_name} created")
        except CollectionInvalid:
            print(f"COURSE GENERATOR [STARTUP]: collection {col_name} already exists")


def create_indexes(db_conn, db_name, collections, indexes):
    for col_name in collections:
        for index, kwargs in indexes[col_name]:
            db_conn[db_name][col_name].create_index(index, **kwargs)
            print(f"COURSE GENERATOR [STARTUP]: index {index} for collection {col_name}")


async def initialize_database(sanic_app):
    print(f"COURSE GENERATOR [STARTUP]: Starting...")
    mongo_url = sanic_app.config["MONGO_URL"]
    redis_url = sanic_app.config["REDIS_URL"]

    print(f"COURSE GENERATOR [STARTUP]: AsyncMotor starting...")
    sanic_app.ctx.mongo_motor = AsyncIOMotorClient(mongo_url)
    print(f"COURSE GENERATOR [STARTUP]: AsyncMotor connected")

    print(f"COURSE GENERATOR [STARTUP]: Redis starting...")
    sanic_app.ctx.redis = redis.from_url(redis_url, decode_responses=True)
    print(f"COURSE GENERATOR [STARTUP]: Redis connected")

    create_database(sanic_app.ctx.mongo_motor, DATABASE_NAME)
    await create_collections(sanic_app.ctx.mongo_motor, DATABASE_NAME, COLLECTIONS)
    create_indexes(sanic_app.ctx.mongo_motor, DATABASE_NAME, COLLECTIONS, INDEXES)

    sanic_app.ctx.mongo = sanic_app.ctx.mongo_motor[DATABASE_NAME]
    await sanic_app.ctx.redis.set("code_1234", dumps({"code": "code_1234",
                                                      "permissions": ["someid123", "otherid123"],
                                                      "role": "admin"}))

    print(f"Course Generator [STARTUP]: Database initialized.")




