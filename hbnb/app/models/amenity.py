#!/usr/bin/python3

import uuid
from . import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
