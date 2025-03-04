import redis
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), decode_responses=True)
r.flushall()