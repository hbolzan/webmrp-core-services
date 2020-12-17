import json
from nameko.exceptions import RemoteError
from .exceptions import handle_exception

def get_form(self, request, name):
    try:
        return json.dumps(self.forms.form(name))
    except RemoteError as e:
        return handle_exception(e)
