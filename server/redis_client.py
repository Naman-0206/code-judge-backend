import redis
r = redis.Redis(host='remotecodeexecution-redis-server-1', port=6379, decode_responses=True)
r.flushall()