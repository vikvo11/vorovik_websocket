from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify=SSLify(app)

@app.route('/')
def index():
    return '<h1>Test flask app!</h1><h2>Ypa!</h2>'

if __name__ =='__main__':
    app.run(host='0.0.0.0',port = 5000)
