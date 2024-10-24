#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity Operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the Amenity')
})

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource)
    api.expect(amenity_model)
    api.response(201, 'Amenity successfully created')
    api.response(400, 'Invalid input data')
    def post(self):
        '''Register Amenity'''
        pass

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        '''Retrieve a list of all amenities'''
        pass

api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        '''Get amenity by id'''
        pass

    api.expect(amenity_model)
    api.response(200, 'Amenity updated successfully')
    api.response(404, 'Amenity not found')
    api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        '''Updated an amenity's info'''
        pass