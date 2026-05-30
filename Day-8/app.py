from flask import Flask, jsonify
from flask_cors import CORS
import redis
import os

app = Flask(__name__)
CORS(app)

r = redis.Redis(
    host="redis-server",
    port=6379,
    decode_responses=True
)

@app.route('/api/join')
def join():
    count = r.incr('user_count')
    return jsonify({
        'status': 'success',
        'users': count
    })

@app.route('/api/leave')
def leave():
    count = r.decr('user_count')

    if int(count) < 0:
        r.set('user_count', 0)
        count = 0

    return jsonify({
        'status': 'success',
        'users': int(count)
    })

@app.route('/api/count')
def count():
    count = r.get('user_count') or 0

    return jsonify({
        'status': 'success',
        'users': int(count)
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
