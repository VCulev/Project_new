from sanic import response


def json_response(status: int, description=None, **kwargs):
    return response.json({'description': description, **kwargs}, status=status)


def j_response(data: dict):
    return response.json(body=data)

