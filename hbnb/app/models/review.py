#!/usr/bin/python3


from . import BaseModel
from . import user
from . import place


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

    def validate_user_and_place(self):
        if not isinstance(self.user, user.User):
            raise ValueError("User must be a valid User instance")

        if not isinstance(self.place, place.Place):
            raise ValueError("Place must be a valid Place instance")

    def proper_text(self, text):
        if not isinstance(text, str):
            raise ValueError("Text must be a string")

        if len(text) <= 0:
            raise ValueError("Text must have some characters")
