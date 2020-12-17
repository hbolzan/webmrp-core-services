import json
from nameko.web.handlers import http
from nameko.rpc import RpcProxy
from config import version
import controllers.forms

class HttpService:
    name = "bff"

    @http("GET", "/api/version")
    def version(self, request):
        return json.dumps({"version": version})

    forms = RpcProxy("forms")

    @http("GET", "/api/forms/<string:name>")
    def get_form(self, request, name):
        return controllers.forms.get_form(self, request, name)
