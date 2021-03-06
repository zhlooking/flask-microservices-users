from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc

from plato import db
from plato.api.models import User
from plato.api.utils import authenticate, is_admin


users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users', methods=['POST'])
@authenticate
def add_user(resp):
    '''Add user info'''
    if is_admin(resp):
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to do that.'
        }
        return make_response(jsonify(response_object)), 403
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': f'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email, password=password))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return make_response(jsonify(response_object)), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, that email already exists.'
            }
            return make_response(jsonify(response_object)), 400
    except exc.IntegrityError as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400
    except ValueError as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''Get single userinfo'''
    response_object = {
        'status': 'fail',
        'message': 'User does not exist.'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return make_response(jsonify(response_object)), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }
            }
            return make_response(jsonify(response_object)), 200
    except ValueError:
        return make_response(jsonify(response_object)), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    '''Get all user info'''
    users = User.query.order_by(User.created_at.desc()).all()
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        users_list.append(user_object)

    response_object = {
        'status': 'success',
        'data': {
            'users': users_list
        }
    }
    return make_response(jsonify(response_object)), 200
