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
