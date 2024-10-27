#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

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
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')
        return amenity

    def get_all_amenities(self):
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if isinstance(amenity, dict) and amenity.get('error'):
            return amenity
        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}, 400
        amenity.name = amenity_data['name']
        return amenity

    def create_place(self, place_data):
        required_fields = ['title', 'description',
                           'price', 'latitude', 'longitude', 'owner_id']

        for field in required_fields:
            if field not in place_data or place_data[field] is None:
                return {"error": f"{field.capitalize()} is required"}, 400

        title = place_data['title']
        description = place_data['description']
        price = place_data['price']
        latitude = place_data['latitude']
        longitude = place_data['longitude']
        owner_id = place_data['owner_id']
        amenity_ids = place_data.get('amenities', [])

        if price < 0:
            return {"error": "Price must be non-negative"}, 400
        if not -90 <= latitude <= 90:
            return {"error": "Latitude must be between -90 and 90"}, 400
        if not -180 <= longitude <= 180:
            return {"error": "Longitude must be between -180 and 180"}, 400

        owner = self.user_repo.get(owner_id)
        if not owner:
            return {"error": "Owner not found"}, 400

        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)
            else:
                return {"error": f"Amenity with ID {amenity_id} not found"}, 400

        place = Place(
            title=title, description=description, price=price,
            latitude=latitude, longitude=longitude, owner=owner
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place.to_dict(), 201

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        for key, value in place_data.items():
            if hasattr(place, key):
                if key == 'price' and value < 0:
                    return {"error": "Price must be non-negative"}, 400
                elif key == 'latitude' and not -90 <= value <= 90:
                    return {"error": "Latitude must be between -90 and 90"}, 400
                elif key == 'longitude' and not -180 <= value <= 180:
                    return {"error": "Longitude must be between -180 and 180"}, 400
                setattr(place, key, value)
        return place.to_dict()
