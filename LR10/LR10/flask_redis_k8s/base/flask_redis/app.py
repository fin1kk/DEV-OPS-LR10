import time
import redis
import socket
import os
from flask import Flask

app = Flask(__name__)

MY_ENV = os.getenv('ENV', 'unknown')
redis_host = os.getenv('REDIS_HOST', 'redis')
cache = redis.Redis(host=redis_host, port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! DROP NEW VERSION!!! I have been seen {} times. My name is: {} MY env: {}'.format(count, socket.gethostname(), MY_ENV)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
