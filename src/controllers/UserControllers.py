from flask import request, json, Response, Blueprint, g
from ..models.Users import UsersModel, UsersSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UsersSchema()


@user_api.route('/add', methods=['POST'])
def create_user():
    """
        Create User Function
    """
    body_json = request.get_json()
    name = body_json['name']
    username = body_json['username']
    password = body_json['password']

    username_in_database = UsersModel.get_user_by_username(username)
    if username_in_database:
        message = {'status': 'error', 'message': 'User already exist, please supply another username!'}
        return custom_response(message, 400)
    else:
        insert_data = UsersModel(name=name, username=username, password=password)
        UsersModel.save(insert_data)
        message = {'status': 'success', 'message': 'User has been created'}
        return custom_response(message, 201)


@user_api.route('/login', methods=['POST'])
def login():
    """
        Create User Function
    """
    body_json = request.get_json()
    username = body_json['username']
    password = body_json['password']

    if not username or not password:
        message = {'status': 'error', 'message': 'You need an username or a password to login!'}
        return custom_response(message, 400)
    else:
        check_username = UsersModel.get_user_by_username(username)
        if not check_username:
            message = {'status': 'error', 'message': 'Invalid credentials!'}
            return custom_response(message, 400)

        if not check_username.check_hash(password):
            message = {'status': 'error', 'message': 'Invalid credentials!'}
            return custom_response(message, 400)

        user_data = user_schema.dump(check_username)
        token = Auth.generate_token(user_data.get('id'))
        message = {'status': 'success', 'message': 'Login success!', 'token': token}
        return custom_response(message, 200)


def custom_response(res, status_code):
    """
        Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

