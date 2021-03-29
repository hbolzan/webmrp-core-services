import json

from .logic.misc import json_to_data
from .config import version
from .helpers.decorators import cors_http
from .helpers.dynamic_proxy import DynamicRpcProxy
from .controllers.generic import handle_request


class HttpService:
    name = "bff"
    dynamic_services = {}
    dynamic_rpc_proxy = DynamicRpcProxy()

    @cors_http("GET", "/api/version")
    def version(self, request):
        return json.dumps({"version": version})

    @cors_http("GET", "/api/forms/<string:name>")
    def get_form(self, request, name):
        forms = self.services("forms")
        return handle_request(lambda: forms.form(name))

    @cors_http("GET,POST", "/api/data/<string:provider>/<string:source>")
    def data__methods(self, request, provider, source):
        data_hub = self.services("data-hub")
        methods = {
            "GET": lambda: data_hub.query(provider, source, request.args),
            "POST": lambda: data_hub.append(provider, source, json_to_data(request)),
        }
        return handle_request(methods.get(request.method))

    @cors_http("GET,PUT,DELETE", "/api/data/<string:provider>/<string:source>/<string:key>")
    def data_one__methods(self, request, provider, source, key):
        data_hub = self.services("data-hub")
        methods = {
            "GET": lambda: data_hub.get_one(provider, source, key),
            "PUT": lambda: data_hub.edit(provider, source, key, json_to_data(request)),
            "DELETE": lambda: data_hub.delete(provider, source, key),
        }
        return handle_request(methods.get(request.method))

    @cors_http("GET", "/api/data/query")
    def query__get(self, request):
        data_hub = self.services("data-hub")
        return handle_request(lambda: data_hub.resolve(request.args.get("query")))

    @cors_http("GET", "/api/validation/<string:provider>/<string:fn>/<string:value>")
    def validation__get(self, request, provider, fn, value):
        service, function = self.validation_parser(provider, fn, value)
        return handle_request(lambda: function(value))

    @cors_http("PUT", "/api/validation/<string:provider>/<string:fn>/<string:value>")
    def validation__put(self, request, provider, fn, value):
        data = json_to_data(request)
        service, function = self.validation_parser(provider, fn, value, data)
        return handle_request(lambda: function(value, data))

    def validation_parser(self, provider, fn, value, data=None):
        service = self.services(provider)
        function = getattr(service, fn)
        return (service, function)

    def services(self, service_name):
        try:
            return self.dynamic_services[service_name]
        except KeyError:
            self.dynamic_services[service_name] = self.dynamic_rpc_proxy(service_name)
            return self.dynamic_services[service_name]
