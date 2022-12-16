import redis

class Redis:

    def __init__(self, root_name, host, port, db) -> None:
        self.root_name = root_name
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)

    class Element:
        def __init__(self, path, pool):
            self.path = path
            self.pool = pool

        def __getitem__(self, key):
            with redis.StrictRedis(connection_pool=self.pool) as r:
                return r.hget(self.path, key)

        def __setitem__(self, key, value):
            with redis.StrictRedis(connection_pool=self.pool) as r:
                return r.hset(self.path, key, value)

        def __str__(self):
            with redis.StrictRedis(connection_pool=self.pool) as r:
                return str(r.hgetall(self.path))

    def delete(self, id):
        with redis.StrictRedis(connection_pool=self.pool) as r:
            r.srem(f"{self.root_name}:keys", id)
            r.delete(f"{self.root_name}:{id}")

    @property
    def keys(self):
        with redis.StrictRedis(connection_pool=self.pool) as r:
            return r.smembers(f"{self.root_name}:keys")

    def __getitem__(self, id):
        return self.Element(f"{self.root_name}:{id}", self.pool)

    def __setitem__(self, id, data: dict):
        with redis.StrictRedis(connection_pool=self.pool) as r:
            r.sadd(f"{self.root_name}:keys", id)
            r.hset(f"{self.root_name}:{id}", mapping=data)

    def clear(self):
        for key in self.keys:
            self.delete(key)
        with redis.StrictRedis(connection_pool=self.pool) as r:
            r.delete(f"{self.root_name}:keys")

