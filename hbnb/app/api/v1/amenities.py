#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        '''Register Amenity'''
        data = request.get_json()
        try:
            amenity = facade.create_amenity(data)
            return amenity, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        # '''Retrieves a list of all Amenities'''
        # amenities = facade.get_all_amenities()
        # return amenities, 200
        return {'message': 'This is a test response from the amenities endpoint.'}, 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        '''Get amenity by id'''
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        '''Update an amenity's info'''
        data = request.get_json()
        result = facade.update_amenity(amenity_id, data)
        if isinstance(result, dict) and 'error' in result:
            return result
        return result, 200
