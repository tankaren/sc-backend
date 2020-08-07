from dotenv import load_dotenv
load_dotenv()

import os
import datetime

from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_json import FlaskJSON
from flask_cors import CORS

from flask_utils import EmailVerifier

application = Flask('application')

class FlaskConfig(object):
    # Flask settings
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_SECRET = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('PASSWORD_SALT')
    JSON_ADD_STATUS = False
    CORS_HEADERS = 'Content-Type'

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

class FlaskExtensions(object):
    def __init__(self, application):
        self.cors = CORS(application)
        self.jwt = JWTManager(application)
        self.mail = Mail(application)
        self.email_verifier = EmailVerifier(application)
        self.flask_json = FlaskJSON(application)

flask_exts = FlaskExtensions(application)