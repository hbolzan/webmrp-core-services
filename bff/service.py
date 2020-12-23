import json
from nameko.web.handlers import HttpRequestHandler
from nameko.rpc import RpcProxy
from config import version
from controllers.generic import handle_request


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
        return handle_request(lambda: self.data_hub.query(provider, source, {}))
