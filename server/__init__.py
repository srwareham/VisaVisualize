import boto.sqs
from flask import Flask
from flask_cors import CORS

application = Flask(__name__)
application.config.from_object('config')
cors = CORS(application)

from app import routes