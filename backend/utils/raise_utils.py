from sanic import exceptions, response


def json_response(status: int, description=None, **kwargs):
    return response.json({'description': description, **kwargs}, status=status)

