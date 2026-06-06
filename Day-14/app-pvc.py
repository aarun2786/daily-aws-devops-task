from flask import Flask
from data import pvc

app = Flask(__name__)

@app.route('/')
def home():
    return pvc.data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
