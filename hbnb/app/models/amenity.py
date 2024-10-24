#!/usr/bin/python3


from . import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        self.name = name
