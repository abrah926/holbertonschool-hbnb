#!/usr/bin/python3


from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
        try:
            title = place_data.get('tittle')
            price = place_data.get('price')
            latitude = place_data.get('latitude')
            longitude = place_data.get('longitude')
            owner_id = place_data.get('owner_id')
            amenities = place_data.get('amenities', [])

            if title is None or price is None or latitude is None or longitude is None or owner_id is None:
                raise ValueError('Missing fields requiered')

            if price < 0:
                raise ValueError('Price must be non-negative')
            if not -90 <= latitude <= 90:
                raise ValueError('Latitude must be between -90 and 90')
            if not -180 <= longitude <= 180:
                raise ValueError("Longitude must be between -180 and 180")

            place = Place(
                title=title,
                description=place_data.get('description', ''),
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=owner_id,
                amenities=amenities
            )
            return place
        except ValueError as e:
            raise ValueError(str(e))

    def get_place(self, place_id):
        '''Retrieves a place by ID, including owner and amenity'''
        place = Place.get_by_id(place_id)
        if place:
            return place
        else:
            raise ValueError('place not found')

    def get_all_places(self):
        '''Retrieves all places'''
        places = Place.get_all()
        return places

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')

        for key, value in place_data.items():
            if hasattr(place, key):
                if key == 'price':
                    if value < 0:
                        raise ValueError('Price must be non-negative')
                elif key == 'latitude':
                    if not -90 <= value <= 90:
                        raise ValueError('latitude must be between -90 and 90')
                elif key == 'longitude':
                    if not -180 <= 180:
                        raise ValueError(
                            'longitude must be between -180 and 180')
                setattr(place, key, value)

        return place
