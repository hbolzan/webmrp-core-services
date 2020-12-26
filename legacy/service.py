import os
import json
from nameko.rpc import rpc

dir_path = os.path.dirname(os.path.realpath(__file__))

class NotFound(Exception):
    pass

class FormsService:
    name = "legacy"

    @rpc
    def query(self, source, params):
        pass

    @rpc
    def get_one(self, source, key):
        pass

    @rpc
    def append(self, source, data):
        pass

    @rpc
    def edit(self, source, key, data):
        pass

    @rpc
    def delete(self, source, key):
        pass
