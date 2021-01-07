import json
from urllib import request
from nameko.rpc import rpc
from .legacy_data_index import data_index


postgrest_base_url = "http://localhost:3000"


def from_index(source_name):
    try:
        return data_index[source_name]["singular"], data_index[source_name]["source"]
    except KeyError:
        return source_name, source_name


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
        namespace, table_name = from_index(source)
        with request.urlopen("{}/{}?id=eq.{}".format(postgrest_base_url, table_name, key)) as resp:
            try:
                return {"data": json.loads(resp.read())}
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
