from dotenv import load_dotenv
load_dotenv()

import os
import datetime

# from init_app import application
from flask import request, jsonify, abort, redirect, \
                  url_for, render_template

from passlib.hash import pbkdf2_sha512 as hash_manager
import mongoengine as mongo

from models import *
from flask_utils import OkResponse, ErrorResponse
# from user_blueprint import user_blueprint
# from catalog_blueprint import catalog_blueprint

from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS

from flask_utils import EmailVerifier

application = Flask(__name__)

class FlaskConfig(object):
    # Flask settings
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_SECRET = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('PASSWORD_SALT')

    # JWT settings
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)

    # Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = f'"sproul.club" <{os.getenv("MAIL_USERNAME")}>'

application.config.from_object(__name__ + '.FlaskConfig')

jwt = JWTManager(application)
mail = Mail(application)
toolbar = DebugToolbarExtension(application)
email_verifier = EmailVerifier(
    secret_key=application.config['SECRET_KEY'], 
    password_salt=application.config['SECURITY_PASSWORD_SALT']
)

CORS(app)

mongo.connect(host=os.getenv('MONGO_URI'))

@application.before_request
def before_request_func():
    if not request.is_json:
        return ErrorResponse(reason='Missing JSON in request').response


# application.register_blueprint(user_blueprint)
# application.register_blueprint(catalog_blueprint)


@application.route('/api/future-sign-up', methods=['POST'])
def sign_up_future():
    json = request.get_json()

    params = ['org-name', 'org-email', 'poc-name', 'poc-email']
    missing_params = []
    for param in params:
        if json.get(param) is None:
            missing_params += [param]

    if len(missing_params) > 0:
        return ErrorResponse(reason=f'Missing the following parameters: {missing_params}', data={'missing': missing_params}).response

    org_name = json['org-name']
    org_email = json['org-email']

    poc_name = json['poc-name']
    poc_email = json['poc-email']

    if len(FutureUser.objects(org_email=org_email)) > 0:
        return ErrorResponse(reason='The organization email has already been registered!').response

    future_user = FutureUser(
        org_name=org_name,
        org_email=org_email,
        poc_name=poc_name,
        poc_email=poc_email,
    )
    future_user.save()

    return OkResponse().response


if __name__ == '__main__':
    application.run(debug=True)