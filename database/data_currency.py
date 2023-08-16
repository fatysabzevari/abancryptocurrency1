import pymongo
import redis


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MongoConnection:
    client = None

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017",
                                          username='username',
                                          password='1234'
                                          ) if not self.client else self.client

        self.db = self.client['db-exchange']
        self.collection = self.db['collection']


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_t):
        self.client.close()


class RedisConnection:
    def __init__(self):
        self.client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True,
            db=0
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_t):
        self.client.close()
