from sanic import Sanic
from json import load
from backend.app_config.routes import route_add_request


def read_config() -> dict:
    file_handler = open("backend/app_config/settings.json", "r")
    server_config = load(file_handler)
    file_handler.close()
    return server_config


def get_app():
    sanic_app = Sanic("CourseGenerator")
    sanic_app.config.update(
        read_config()
    )

    sanic_app.add_route(route_add_request, "/api/add_request", methods=["GET"], ctx_refsanic=sanic_app)

    return sanic_app
