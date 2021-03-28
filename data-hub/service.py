import json
import base64

from nameko.rpc import rpc, RpcProxy
from .helpers.dynamic_proxy import DynamicRpcProxy
from .controllers import resolver


class NotFound(Exception):
    pass


class DataHubService:
    name = "data-hub"
    dynamic_services = {}
    dynamic_rpc_proxy = DynamicRpcProxy()

    @rpc
    def query(self, provider_name, source, params):
        return self.provider(provider_name).query(source, params)

    @rpc
    def get_one(self, provider_name, source, key):
        return self.provider(provider_name).get_one(source, key)

    @rpc
    def resolve(self, query_encoded):
        query = json.loads(base64.b64decode(query_encoded))
        return {
            "status": "OK",
            "data": resolve(self.provider, query)
        }

    @rpc
    def append(self, provider_name, source, data):
        return self.provider(provider_name).append(source, data)

    @rpc
    def edit(self, provider_name, source, key, data):
        return self.provider(provider_name).edit(source, key, data)

    @rpc
    def delete(self, provider_name, source, key):
        return self.provider(provider_name).delete(source, id, params = {})

    def provider(self, service_name):
        try:
            return self.dynamic_services[service_name]
        except KeyError:
            self.dynamic_services[service_name] = self.dynamic_rpc_proxy(service_name)
            return self.dynamic_services[service_name]
