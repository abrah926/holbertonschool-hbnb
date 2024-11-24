from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
import logging

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Cannot review your own place or duplicate')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    logging.basicConfig(level=logging.DEBUG)

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review by ID."""
        current_user = get_jwt_identity()  # JWT identity contains the user ID.
        current_user_id = current_user.get("id")

        # Fetch the review from the database
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Log IDs for debugging
        logging.debug(f"Review User ID: {review.user_id}")
        logging.debug(f"Current User ID: {current_user_id}")

        # Check if the current user owns the review
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized to modify this review'}, 403

        # Update review fields
        review_data = api.payload
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        # Save the changes to the database
        db.session.commit()

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized to delete this review')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized to delete this review'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'Place not found'}, 404
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200
