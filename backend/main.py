from app_config.configure import get_app

sanic_task = get_app()


def run_api():
    get_option = sanic_task.config.get
    sanic_task.run(
        host=get_option("HOST"),
        port=get_option("PORT"),
        debug=get_option("DEBUG"),
        workers=get_option("WORKERS"),
        fast=get_option("FAST")
    )


if __name__ == '__main__':
    run_api()
