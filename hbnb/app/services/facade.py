#!/usr/bin/python3
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models import db


class HBnBFacade:
    def __init__(self):
        # Initialize repositories for each model using SQLAlchemyRepository
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.review_repo = SQLAlchemyRepository(Review)

    # User-related methods
    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],  # Raw password passed here
            is_admin=user_data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def authenticate_user(self, email, password):
        user = self.user_repo.get_by_attribute('email', email)
        # Use the verify_password method
        if user and user.verify_password(password):
            return user
        return None

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None

    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Invalid owner ID")

        amenities = [self.amenity_repo.get(aid)
                     for aid in place_data['amenities']]
        if None in amenities:
            raise ValueError("Invalid amenity ID in amenities list")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data["owner_id"],
        )
        place.amenities = amenities

        # Save the Place to the database
        db.session.add(place)
        db.session.commit()

        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        # Handle amenities separately
        if "amenities" in place_data:
            amenity_ids = place_data.get("amenities", [])
        # Fetch Amenity instances from the IDs
            amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all()

            if len(amenities) != len(amenity_ids):
                raise ValueError("One or more amenities not found")

            place.amenities = amenities  # Assign Amenity instances to the relationship

        # Update other fields in the Place object
        for key, value in place_data.items():
            if hasattr(place, key) and key != "amenities":
                setattr(place, key, value)

        db.session.commit()
        return place

    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user:
            raise ValueError("Invalid user ID")
        if not place:
            raise ValueError("Invalid place ID")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        return [review for review in self.get_all_reviews() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        review = self.get_review(review_id)
        if review:
            review.update(review_data)
            return review
        return None

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        review = self.get_review(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False
