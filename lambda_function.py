from flask import Flask
from serverless_wsgi import handle_request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask + serverless-wsgi in a Lambda layer!"

def lambda_handler(event, context):
    return handle_request(app, event, context)
