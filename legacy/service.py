import json
from urllib import request
from nameko.rpc import rpc


postgrest_base_url = "http://localhost:3000"

class NotFound(Exception):
    pass

class LegacyService:
    name = "legacy"

    @rpc
    def query(self, source, params):
        with request.urlopen("{}/{}".format(postgrest_base_url, source)) as resp:
            return {"data": json.loads(resp.read())}

    @rpc
    def get_one(self, source, key):
        url = "{}/{}?id=eq.{}".format(postgrest_base_url, source, key)
        with request.urlopen("{}/{}/?id=eq.{}".format(postgrest_base_url, source, key)) as resp:
            try:
                return {"data": json.loads(resp.read())[0]}
            except IndexError:
                raise NotFound

    @rpc
    def append(self, source, data):
        pass

    @rpc
    def edit(self, source, key, data):
        pass

    @rpc
    def delete(self, source, key):
        pass
