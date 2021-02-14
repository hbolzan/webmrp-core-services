import json
import hashlib
import psycopg2
import psycopg2.extras


class Transaction:
    def __init__(self, params):
        connection = Connection()
        self.conn_fn = lambda : connection.connection(params)

    def query(self, sql):
        with self.conn_fn().cursor(cursor_factory=psycopg2.extras.RealDictCursor) as c:
            c.execute(sql)
            return json.dumps(c.fetchall())


class Connection:
    connections = {}

    def connection(self, params):
        hash = self.connection_hash(params)
        try:
            return self.live_connection(self.connections[hash], hash, params)
        except KeyError:
            return self.connect(hash, params)

    def connection_hash(self, params):
        s = "".join(map(lambda k: str(params[k]), params.keys()))
        return hashlib.md5(s.encode()).hexdigest()

    def live_connection(self, conn, hash, params):
        return conn if self.alive(conn) else self.connect(hash, params)

    def alive(self, conn):
        try:
            conn.isolation_level
            return true
        except psycopg2.OperationalError:
            return false

    def connect(self, hash, params):
        self.connections[hash] = psycopg2.connect(**params)
        return self.connections[hash]
