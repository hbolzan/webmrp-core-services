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

    @cors_http("GET", "/api/data/<string:provider>/<string:source>")
    def get_data(self, request, provider, source):
        return handle_request(lambda: self.data_hub.query(provider, source, request.args))

    @cors_http("GET", "/api/data/<string:provider>/<string:source>/<string:key>")
    def get_data(self, request, provider, source, key):
        return handle_request(lambda: self.data_hub.get_one(provider, source, key))

    @cors_http("POST", "/api/data/<string:provider>/<string:source>")
    def post_data(self, request, provider, source):
        print(json_to_data(request))
        return handle_request(lambda: self.data_hub.append(provider, source, json_to_data(request)))

    @cors_http("PUT", "/api/data/<string:provider>/<string:source>/<string:key>")
    def put_data(self, request, provider, source, key):
        return handle_request(lambda: self.data_hub.edit(provider, source, key, json_to_data(request)))

    @cors_http("DELETE", "/api/data/<string:provider>/<string:source>/<string:key>")
    def delete_data(self, request, provider, source, key):
        return handle_request(lambda: self.data_hub.delete(provider, source, key))
