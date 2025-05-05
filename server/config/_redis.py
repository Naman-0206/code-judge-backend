import redis
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), 
    port=os.getenv("REDIS_PORT", 6379),
    password=os.getenv("REDIS_PASSWORD", None),
    username=os.getenv("REDIS_USER", None),
    ssl=True,
    decode_responses=True
    )