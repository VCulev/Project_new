from sanic import Sanic
from json import load
from backend.app_config.routes import register_user, login_user, user_input, display_results


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

    sanic_app.add_route(register_user, "/api/register_user", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(login_user, "/api/login_user", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(user_input, "/api/user_input", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(display_results, "/api/display_results", methods=["GET"], ctx_refsanic=sanic_app)

    return sanic_app
