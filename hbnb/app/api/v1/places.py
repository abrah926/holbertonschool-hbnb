from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import jsonify
from app.api.v1 import places_ns
from flask import request

api = Namespace('places', description='Place operations')


facade = HBnBFacade()

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})


place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@places_ns.route('/')
class PlaceResource(Resource):
    @places_ns.expect(place_model)
    @places_ns.response(201, 'Place successfully created')
    @places_ns.response(400, 'Invalid input data')
    def post(self):
        place_data = request.get_json()
        try:
            result, status = facade.create_place(place_data)
            if status == 201:
                return result.to_dict(), status
            return result, status
        except ValueError as e:
            return {'message': str(e)}, 400

    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        try:
            places = facade.get_all_places()

            return [place.to_dict() for place in places], 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            return place.to_dict(), 200
        except ValueError:
            return {'message': 'Place not found'}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload

        try:
            place = facade.update_place(place_id, data)
            return place.to_dict(), 200
        except ValueError as e:
            return {'message': str(e)}, 400
