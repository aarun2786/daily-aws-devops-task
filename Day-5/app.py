from flask import Flask
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='redis', port=6379)

@app.route('/')
def home():
    redis_client.incr('hits')
    return f"Container Visits: {redis_client.get('hits').decode('utf-8')}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
