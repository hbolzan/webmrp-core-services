from nameko.extensions import DependencyProvider
from nameko.rpc import RpcProxy, ServiceProxy, ReplyListener


class RpcProxyFactory(object):
    def __init__(self, worker_ctx, reply_listener):
        self.worker_ctx = worker_ctx
        self.reply_listener = reply_listener

    def __call__(self, target_service):
        return ServiceProxy(self.worker_ctx, target_service, self.reply_listener)


class DynamicRpcProxy(DependencyProvider):
    rpc_reply_listener = ReplyListener()

    def get_dependency(self, worker_ctx):
        return RpcProxyFactory(worker_ctx, self.rpc_reply_listener)
