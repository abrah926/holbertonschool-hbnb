from flask import Blueprint
from flask_restx import Api
from .v1.users import api as users_api
from .v1.amenities import api as amenities_api


def create_api(app):
    api = Api(app, version='1.0', title='HBnB API',
              description='A simplified AirBnB API')
    api.add_namespace(users_api, path='/api/v1/users')
    api.add_namespace(amenities_api, path='/api/v1/amenities')
