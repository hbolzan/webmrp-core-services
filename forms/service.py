import os
import json
from nameko.rpc import rpc

dir_path = os.path.dirname(os.path.realpath(__file__))

class NotFound(Exception):
    pass

class FormsService:
    name = "forms"

    @rpc
    def form(self, name):
        try:
            with open("{}/resources/{}.json".format(dir_path, name)) as f:
                return {
                    "status": "OK",
                    "form": json.loads(f.read())
                }
        except FileNotFoundError:
            raise NotFound
