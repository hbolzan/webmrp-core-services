import json


def json_to_data(request):
    if request.mimetype == "application/json":
        try:
            return json.loads(request.data)
        except json.JSONDecodeError:
            return None
