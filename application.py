from dotenv import load_dotenv
load_dotenv()

import os
import datetime

from init_app import application
from flask import request

from flask_json import as_json, JsonError

import mongoengine as mongo

from models import *
# from user_blueprint import user_blueprint
# from catalog_blueprint import catalog_blueprint

from flask_utils import ParamChecker

mongo.connect(host=os.getenv('MONGO_URI'))

@application.before_request
def before_request_func():
    if request.method != 'OPTIONS' and not request.is_json:
        raise JsonError(reason='JSON is required!')


# application.register_blueprint(user_blueprint)
# application.register_blueprint(catalog_blueprint)

application.config['CORS_HEADERS'] = '*'

@as_json
@application.route('/api/future-sign-up', methods=['POST', 'OPTIONS'])
def sign_up_future():
    json = request.get_json()

    params = ['org-name', 'org-email', 'poc-name', 'poc-email']
    missing_params_error = ParamChecker(json).verify_with(params)
    if missing_params_error is not None:
        raise missing_params_error

    org_email = json['org-email']
    if len(FutureUser.objects(org_email=org_email)) > 0:
        raise JsonError(reason='The organization email has already been registered!')

    try:
        FutureUser(
            org_name=json['org-name'],
            org_email=org_email,
            poc_name=json['poc-name'],
            poc_email=json['poc-email'],
        ).save()
    except mongo.errors.ValidationError as ex:
        raise JsonError(reason='Both the organization email and POC email must be valid!')

    return {'status': 'ok'}


if __name__ == '__main__':
    application.run(debug=True)