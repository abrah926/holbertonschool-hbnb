#!/usr/bin/python3


from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, updated_data):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in updated_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                return {'error': f'Invalid attribute: {key}'}, 400
        return user

    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}, 400
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return{'error': 'Amenity not found'}, 404
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if isinstance(amenity, dict) and amenity.get('error'):
            return amenity
        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}, 400
        amenity.name = amenity_data['name']
        return amenity
