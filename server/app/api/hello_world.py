from flask import abort, Blueprint, send_file
from flask.ext import restful
from flask.ext.restful.reqparse import RequestParser
import numpy as np

from app import application

hello_world_blueprint = Blueprint('hello_world', __name__)
hello_world_api = restful.Api(hello_world_blueprint)

class HelloWorld(restful.Resource):
	def post(self):
		"""
        Returns the number posted
        Args:
            number:  Number posted to server.
        """
		parser = RequestParser()
		parser.add_argument('name', required=True, type=str, location='json', help='number is required')
		args = parser.parse_args()
		return 'Hello ' + args.name, 200

hello_world_api.add_resource(HelloWorld, '/name')