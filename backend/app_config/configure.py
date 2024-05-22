from sanic import Sanic
from sanic_ext import Extend
from json import load
from backend.app_config.routes import (register_user, login_user, add_response_headers,
                                       handle_options_route, get_quiz, scrape_questions,
                                       logout_user)
from backend.mongodb.startup import initialize_database
from sanic_cors import CORS


def read_config() -> dict:
    file_handler = open("app_config/settings.json", "r")
    server_config = load(file_handler)
    file_handler.close()
    return server_config


def get_app():
    sanic_app = Sanic("QuizGenerator")
    sanic_app.config.update(read_config())

    cors_config = {
        "origins": "http://localhost:63342",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
    }

    CORS(sanic_app, resources={r"/api/*": cors_config})

    @sanic_app.middleware('response')
    async def add_cors_headers(request, response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:63342'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    sanic_app.register_listener(initialize_database, "before_server_start")

    Extend(sanic_app)

    sanic_app.add_route(register_user, "/api/register_user", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(login_user, "/api/login_user", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(logout_user, "api/logout_user", methods=["POST"], ctx_refsanic=sanic_app)
    sanic_app.add_route(get_quiz, "/api/quiz", methods=["GET"], ctx_refsanic=sanic_app)
    sanic_app.add_route(scrape_questions, "api/scrape-newsletter", methods=["GET"], ctx_refsanic=sanic_app)
    sanic_app.add_route(handle_options_route, "/api/register_user", methods=["OPTIONS"], ctx_refsanic=sanic_app,
                        name="handle_options_register_user")
    sanic_app.add_route(handle_options_route, "/api/login_user", methods=["OPTIONS"], ctx_refsanic=sanic_app,
                        name="handle_options_login_user")
    sanic_app.add_route(handle_options_route, "api/scrape-newsletter", methods=["OPTIONS"], ctx_refsanic=sanic_app,
                        name="handle_options_scrape_newsletter")
    sanic_app.add_route(handle_options_route, "api/logout_user", methods=["OPTIONS"], ctx_refsanic=sanic_app,
                        name="handle_options_logout_user")
    sanic_app.on_response(add_response_headers)

    return sanic_app
