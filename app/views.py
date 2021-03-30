from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource, abort

from app import db, app
from app.models import File

import os
import threading


USERNAME = 'tester'
PASSWORD = 'tester123'


class Authorization(Resource):
	def post(self):
		args = dict(request.args)
		if args['username'] != USERNAME or args['password'] != PASSWORD:
			return jsonify(
				{
					'error': 'Invalid username or password',
					'status_code': 400,
				}
			)
		return jsonify(access_token=create_access_token(identity = USERNAME))


class FileOperation(Resource):
	@jwt_required()
	def get(self, filename):
		file = File.query.get(filename)
		if file:
			return jsonify(file.as_dict())
		return jsonify(
			{
				'error': 'File is not exist',
				'status_code': 400,
			}
		)

	def post(self, filename):
		extension = filename.split('.')[-1].lower()
		file = File()
		db.session.add(file)
		db.session.commit()
		with open(os.path.join(app.config['UPLOAD_DIR'], '.'.join([str(file.id), extension])), "wb") as book:
			book.write(request.data)
		response = jsonify(file.as_dict())
		response.status_code = 201
		file.extension = extension
		thread = threading.Thread(file.process())
		thread.start()
		return response