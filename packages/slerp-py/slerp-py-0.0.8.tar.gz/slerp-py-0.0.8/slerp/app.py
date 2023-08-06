import json
import os
from sqlalchemy.exc import DatabaseError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from consul import Consulate
from exception import ValidationException, CoreException
from logger import logging
from response import JsonResponse

log = logging.getLogger(__name__)

DEFAULT_CONFIG = 'config.json'
if not os.path.exists(DEFAULT_CONFIG):
	raise RuntimeError('please create config.json file in your project root folder')


def init_apps(configuration):
	apps = Flask(__name__)
	consul = Consulate(app=apps)
	consul.load_config(namespace=configuration['namespace'])
	consul.register(name=configuration['name'], interval=configuration['interval'],
	                httpcheck=configuration['health'])
	return apps


json_file = open(DEFAULT_CONFIG, 'rb')
config = json.load(json_file)
json_file.close()
app = init_apps(config)
db = SQLAlchemy(app=app)
app.response_class = JsonResponse


@app.errorhandler(Exception)
# noinspection PyTypeChecker
def handle_error(error):
	msg = {'status': 'FAIL'}
	if type(error) is TypeError:
		msg.update({'message': 'type.error'})
	elif type(error) is ValidationException:
		msg.update({'message': error.message})
		if error.key is not None:
			msg.update({'key': error.key})
			pass
	elif type(error) is CoreException:
		msg.update({'message': error.message})
	else:
		message = [str(x) for x in error.args]
		msg.update({'message': message})
	
	log.error(error, exc_info=True)
	return msg


@app.after_request
def session_commit(response):
	if 'AUTO_ROLLBACK' in app.config and app.config['AUTO_ROLLBACK']:
		db.session.rollback()
	else:
		try:
			db.session.commit()
		except DatabaseError:
			db.session.rollback()
	return response


def run(**kwargs):
	kwargs.update({'port': app.config['SERVER_PORT']})
	if 'SERVER_HOST' in app.config:
		kwargs.update({'host': app.config['SERVER_HOST']})
	app.run(**kwargs)
