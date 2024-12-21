import redis
import json
r = redis.Redis(host='remotecodeexecution-redis-server-1', port=6379, decode_responses=True)

def save_result(key, value):
    r.set(key, json.dumps(value))