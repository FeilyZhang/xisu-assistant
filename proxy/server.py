from tools.redisClient import RedisClient
redis_conn = RedisClient()


def get_proxy():
    proxy = redis_conn.pop_proxy().decode("utf8")
    if proxy[:5] == "https":
        return {"https": proxy}
    else:
        return {"http": proxy}
