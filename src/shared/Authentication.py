import jwt
import os
import datetime
import pytz
from flask import json, Response, request, g
from functools import wraps
from ..models.Users import UsersModel

tz = pytz.timezone('Asia/Jakarta')
ct = datetime.datetime.now(tz=tz)
ctNambahSehari = datetime.datetime.now(tz=tz) + datetime.timedelta(days=1)
jakarta_now = ct.strftime('%Y-%m-%d %H:%m:%S')
jakarta_besok = ctNambahSehari.strftime('%Y-%m-%d %H:%m:%S')


class Auth():
    """
        Auth class
    """

    @staticmethod
    def generate_token(user_id):
        """
            Generate token method
        """
        try:
            payload = {
                'exp': jakarta_besok,
                'iat': jakarta_now,
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            ).decode("utf-8")
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'status': 'error', 'message': 'Error in generating user token!'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        """
            Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as ese:
            re['error'] = {'status': 'error', 'message': 'Token expired, please login again!'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'status': 'error', 'message': 'Invalid token, please try again with a new token!'}

    # Decorator
    @staticmethod
    def auth_required(func):
        """
            Auth decorator
        """

        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'status': 'error',
                                         'message': 'Authentication token is not available, please login to get one'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = UsersModel.get_one_user(user_id)

            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'status': 'error', 'message': 'user does not exist, invalid token'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)

        return decorated_auth
