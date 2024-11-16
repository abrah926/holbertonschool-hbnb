#!/usr/bin/python3


from . import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def use_proper_rating_stoopid(self):
        if not isinstance(self.rating, int):
            raise ValueError("Rating must be an integer")

        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 to 5")

    def validate_text(self):
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("Review text must be a non-empty string.")

    def validate_user_id(self):
        if not isinstance(self.user.id, str) or not self.user.id:
            raise ValueError("User ID must be valid format.")

    def validate_place_id(self):
        if not isinstance(self.place.id, str) or not self.place.id:
            raise ValueError("Place ID must be valid format.")

    @staticmethod
    def _is_valid_uuid(value):
        try:
            import uuid
            uuid.UUID(value)
            return True
        except ValueError:
            return False

    def validate_all(self):
        self.validate_text()
        self.use_proper_rating_stoopid()
        self.validate_user_id()
        self.validate_place_id()

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
