#!/usr/bin/python3
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from . import BaseModel
from app.extensions import db, bcrypt
import uuid


class User(BaseModel):
    __tablename__ = 'users'

    def __init__(self, first_name, last_name, email, is_admin=False, password=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []

        if password:
            self.password_hash = generate_password_hash(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)
