from nameko.rpc import rpc, RpcProxy

class NotFound(Exception):
    pass

class DataHubService:
    name = "data-hub"
    providers = {
        "legacy": RpcProxy("legacy"),
    }

    def provider(self, provider_name):
        try:
            return self.providers[provider_name]
        except KeyError:
            raise NotFound

    @rpc
    def query(self, provider_name, source, params):
        return self.provider(provider_name).query(source, params)

    @rpc
    def get_one(self, provider_name, source, key):
        return self.provider(provider_name).get_one(source, key)

    @rpc
    def append(self, provider_name, source, data):
        return self.provider(provider_name).append(source, data)

    @rpc
    def edit(self, provider_name, source, key, data):
        return self.provider(provider_name).edit(source, key, data)

    @rpc
    def delete(self, provider_name, source, key):
        return self.provider(provider_name).delete(source, id, params = {})
