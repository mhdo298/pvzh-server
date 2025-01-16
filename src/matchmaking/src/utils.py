from flask import request


def get_id():
    return request.headers.get("eadp-persona-id")


