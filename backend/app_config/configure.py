from sanic import Sanic
from json import load
from backend.app_config.routes import (register_route, login_user, add_response_headers,
                                       handle_route)
from backend.mongodb.startup import initialize_database
from sanic_cors import CORS


def read_config() -> dict:
    file_handler = open("backend/app_config/settings.json", "r")
    server_config = load(file_handler)
    file_handler.close()
    return server_config


def get_app():
    sanic_app = Sanic("CourseGenerator")
    sanic_app.config.update(read_config())
    CORS(sanic_app)
    sanic_app.register_listener(initialize_database, "before_server_start")
    sanic_app.add_route(register_route, "/api/register_user", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(login_user, "/api/login_user", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(handle_route, "/api/register_user", methods=["OPTIONS"], ctx_refsanic=sanic_app,
                        name="handle_options_register_user")
    sanic_app.add_route(handle_route, "/api/login_user", methods=["OPTIONS"], ctx_refsanic=sanic_app,
                        name="handle_options_login_user")
    sanic_app.on_response(add_response_headers)

    return sanic_app

