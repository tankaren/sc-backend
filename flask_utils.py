from itsdangerous import URLSafeTimedSerializer
from flask import Flask, jsonify
from flask_json import JsonError


class ParamChecker:
    def __init__(self, json):
        self.json = json

    def verify_with(self, params):
        missing_params = []
        for param in params:
            if self.json.get(param) is None:
                missing_params += [param]

        if len(missing_params) > 0:
            raise JsonError(reason=f'Missing the following parameters: {missing_params}', data={'missing': missing_params})
        return None


class EmailVerifier:
    def __init__(self, app=None):
        if isinstance(app, Flask):
            self.init_app(app)

    def init_app(self, app):
        if isinstance(app, Flask):
            secret_key = app.config['SECRET_KEY']
            self.serializer = URLSafeTimedSerializer(secret_key)
            self.pass_salt = app.config['SECURITY_PASSWORD_SALT']

    def generate_token(self, email):
        serializer.dumps(email, salt=self.pass_salt)

    def confirm_token(self, token, expiration=3600):
        try:
            email = serializer.loads(token, salt=self.pass_salt, max_age=expiration)
        except:
            return None
        return email


class EmailSender:
    def __init__(self, app):
        if isinstance(app, Flask):
            self.init_app(app)

    def init_app(self, app):
        if isinstance(app, Flask):
            self.sender = app.config['MAIL_DEFAULT_SENDER']

    def send(self, recipients, subject, body):
        msg = Message(
            subject=subject,
            recipients=recipients,
            html=body,
            sender=self.sender
        )

        mail.send(msg)
