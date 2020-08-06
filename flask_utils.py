from itsdangerous import URLSafeTimedSerializer
from flask import jsonify

class EmailVerifier:
    def __init__(self, secret_key, password_salt):
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.pass_salt = password_salt

    def generate_token(self, email):
        serializer.dumps(email, salt=self.pass_salt)

    def confirm_token(self, token, expiration=3600):
        try:
            email = serializer.loads(token, salt=self.pass_salt, max_age=expiration)
        except:
            return None
        return email
        

class OkResponse:
    def __init__(self, status=200):
        self.status = status

    @property
    def response(self):
        return jsonify({ 'status': 'ok' }), self.status


class ErrorResponse:
    def __init__(self, reason='Unknown', status=400, data=None):
        self.reason = reason
        self.status = status
        self.data = data or None

    @property
    def response(self):
        response = {
            'status': 'error',
            'reason': self.reason
        }

        if self.data is not None:
            response['data'] = self.data

        return jsonify(response), self.status