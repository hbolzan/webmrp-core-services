import json
from nameko.exceptions import RemoteError
from .exceptions import handle_exception


def handle_request(req_fn):
    try:
        return json.dumps(req_fn())
    except RemoteError as e:
        return handle_exception(e)
