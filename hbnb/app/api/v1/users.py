#!/usr/bin/python3

from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/login')
class UserLoginResource(Resource):
    """Login an existing user"""
    @api.expect(login_model, validate=True)
    @api.response(200, 'User successfully logged in')
    @api.response(401, 'Invalid credentials')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Authenticate the user and return a JWT token"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = facade.authenticate_user(email, password)
        if not user:
            return {'error': 'Invalid credentials'}, 401
        access_token = create_access_token(identity=user.id)
        return {
            'access_token': access_token
        }, 200


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user({
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'email': user_data['email'],
            'password': user_data['password']
        })

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        user_data = api.payload
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        user.update(user_data)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
