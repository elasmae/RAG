import redis
from ..settings import settings

_r = None

def get_redis():
    global _r
    if _r is None:
        _r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
    return _r
