import json
from nameko.rpc import rpc

class NotFound(Exception):
    pass

class FormsService:
    name = "forms"

    @rpc
    def form(self, name):
        try:
            with open("./resources/{}.json".format(name)) as f:
                return {
                    "status": "OK",
                    "form": json.loads(f.read())
                }
        except FileNotFoundError:
            raise NotFound
