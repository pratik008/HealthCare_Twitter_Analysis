#!flask/bin/python
from flask import Flask
context = ('thcap.key','/etc/ssl/certs/ssl-cert-snakeoil.pem')

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=443,ssl_context=context,threaded=True,debug=True)
