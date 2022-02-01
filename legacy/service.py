import os
from toolz.itertoolz import first, second
from urllib import request
from nameko.rpc import rpc
from .settings import databases
from .components.connection import Transaction
from .controllers import resources
from .logic import query
from .logic import response
from .logic import resolver
from .legacy_resources import resources_index


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
default_select = lambda resource_name: "select * from {}".format(resource_name) + " {where} {order_by}"
default_delete = lambda resource_name: "delete from {}".format(resource_name) + " {where}"

transaction = Transaction(databases["default"])


class NotFound(Exception):
    pass


class LegacyService:
    name = "legacy"

    @rpc
    def query(self, resource_name, params):
        return response.to_response(transaction.query(
            resources.resource_to_sql(ROOT_PATH, resource_name, "select", default_select(resource_name)).format(
                where=query.where(query.params_to_search_condition(params)),
                order_by=""
            )
        ))

    @rpc
    def get_one(self, resource_name, key):
        namespace, table_name, query_pk, pk = query.from_index(resources_index, resource_name)
        return response.to_response(transaction.query(
            resources.resource_to_sql(
                ROOT_PATH,
                resource_name,
                "select",
                default_select(resource_name)
            ).format(
                where=query.where("{}={}".format((query_pk or pk), key)),
                order_by=""
            )
        ))

    @rpc
    def resolve(self, query):
        return transaction.query(
            resolver.to_sql(resolver.resolve([self.resolver_source(first(query)), second(query)]))
        )

    def resolver_source(self, resource_name):
        return "({}) q0".format(
            resources.resource_to_sql(
                ROOT_PATH,
                resource_name,
                "select",
                default_select(resource_name)
            ).format(where="", order_by="")
        )

    @rpc
    def append(self, source, data):
        pass

    @rpc
    def edit(self, source, key, data):
        pass

    @rpc
    def delete(self, resource_name, key):
        namespace, table_name, pk = query.from_index(resources_index, resource_name)
        sql = resources.resource_to_sql(
            ROOT_PATH,
            resource_name,
            "delete",
            default_delete(resource_name)
        ).format(
                where=query.where("{}={}".format(pk, key)),
        )
        print(sql)
        transaction.execute(sql)
        return response.to_response({})
