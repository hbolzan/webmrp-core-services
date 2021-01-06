import json
from nameko.web.handlers import HttpRequestHandler
from nameko.rpc import RpcProxy
from .config import version
from .controllers.generic import handle_request


def json_to_data(request):
    if request.mimetype == "application/json":
        return json.loads(request.data)

class CorsHttpRequestHandler(HttpRequestHandler):
    def handle_request(self, request):
        self.request = request
        return super(CorsHttpRequestHandler, self).handle_request(request)

    def response_from_result(self, *args, **kwargs):
        response = super(CorsHttpRequestHandler, self).response_from_result(*args, **kwargs)
        response.headers.add("Access-Control-Allow-Headers",
                             self.request.headers.get("Access-Control-Request-Headers"))
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


cors_http = CorsHttpRequestHandler.decorator


class HttpService:
    name = "bff"
    forms = RpcProxy("forms")
    data_hub = RpcProxy("data-hub")

    @cors_http("GET", "/api/version")
    def version(self, request):
        return json.dumps({"version": version})

    @cors_http("GET", "/api/forms/<string:name>")
    def get_form(self, request, name):
        return handle_request(lambda: self.forms.form(name))

    @cors_http("GET,POST", "/api/data/<string:provider>/<string:source>")
    def data__methods(self, request, provider, source):
        methods = {
            "GET": lambda: self.data_hub.query(provider, source, request.args),
            "POST": lambda: self.data_hub.append(provider, source, json_to_data(request)),
        }
        return handle_request(methods.get(request.method))

    @cors_http("GET,PUT,DELETE", "/api/data/<string:provider>/<string:source>/<string:key>")
    def data_one__methods(self, request, provider, source, key):
        methods = {
            "GET": lambda: self.data_hub.get_one(provider, source, key),
            "PUT": lambda: self.data_hub.edit(provider, source, key, json_to_data(request)),
            "DELETE": lambda: self.data_hub.delete(provider, source, key),
        }
        return handle_request(methods.get(request.method))
