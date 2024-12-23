import redis
import json
import os
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True)

def save_result(key, value):
    r.set(key, json.dumps(value))