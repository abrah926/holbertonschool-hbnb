#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from werkzeug.security import generate_password_hash, check_password_hash


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        if 'password' in user_data:
            if 'password' in user_data:
                password_hash = generate_password_hash(
                    user_data.pop('password'))
            user_data['password_hash'] = password_hash
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def authenticate_user(self, email, password):
        user = self.user_repo.get_by_attribute('email', email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, amenity_data):

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):

        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):

        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):

        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None

    def create_place(self, place_data):

        owner = self.user_repo.get(place_data['owner_id'])

        if not owner:
            raise ValueError("Invalid owner ID")

        amenities = [self.amenity_repo.get(some_id)
                     for some_id in place_data['amenities']]
        if None in amenities:
            raise ValueError("Invalid amenity ID in amenities list")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            amenities=amenities
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):

        return self.place_repo.get(place_id)

    def get_all_places(self):

        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):

        place = self.get_place(place_id)
        if place:
            place.update(place_data)
            return place
        return None

    def create_review(self, review_data):
        place = self.place_repo.get(review_data['place_id'])

        if not place:
            raise ValueError("Invalid place ID")

        user = self.user_repo.get(review_data['user_id'])

        if not user:
            raise ValueError("Invalid user ID")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.get_all_reviews() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if review:
            review.update(review_data)
            return review
        return None

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False
