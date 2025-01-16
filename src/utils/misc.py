from quart import request


def get_id():
    return request.headers.get("eadp-persona-id")

def merge_json(base, head):
    for key in head:
        if type(head[key]) == dict:
            if key in base:
                merge_json(base[key], head[key])
            else:
                base[key] = head[key]
        elif type(head[key]) == list:
            if key not in base:
                base[key] = []
            base[key] += head[key]
        else:
            base[key] = head[key]