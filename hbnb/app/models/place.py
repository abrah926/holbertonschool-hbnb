from app.extensions import db
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, String, ForeignKey, Float, Text

# Many-to-Many relationship table
place_amenities = Table(
    'place_amenities',
    db.metadata,
    Column('place_id', String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(36), ForeignKey(
        'amenities.id'), primary_key=True)
)


class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    title = db.Column(String(128), nullable=False)
    description = db.Column(Text, nullable=True)
    price = db.Column(Float, nullable=False)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)
    owner_id = db.Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = relationship('User', backref='places', lazy=True)
    amenities = relationship(
        'Amenity',
        secondary=place_amenities,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id

    def validate_title(self, title):
        """Validate title field."""
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be less than 100 characters")
        return title

    def validate_price(self, price):
        """Validate price field."""
        if price < 0:
            raise ValueError("Price must be a non-negative value")
        return price

    def validate_latitude(self, latitude):
        """Validate latitude field."""
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude

    def validate_longitude(self, longitude):
        """Validate longitude field."""
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def update(self, data):
        """Update the Place object with the provided data."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
