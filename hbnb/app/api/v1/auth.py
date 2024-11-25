#!/usr/bin/python3
from app.extensions import db, bcrypt
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask import jsonify, make_response


api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token in a cookie"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity={'id': str(user.id), 'is_admin': user.is_admin})

        response = make_response(jsonify({'message': 'Login successful'}))
        response.set_cookie(
            'token',
            access_token,
            httponly=True,
            secure=False,   # Use True in production with HTTPS
            samesite='None',  # Allow cross-origin requests
            domain='127.0.0.1:5000',
        )
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        # DEBUG: Log all response headers to console
        print("Response Headers:", dict(response.headers))

        # Add headers to the response body for debugging purposes
        response_body = {
            'message': 'Login successful',
            # Add headers to response body
            'headers': {k: v for k, v in response.headers.items()}
        }
        return jsonify(response_body)
