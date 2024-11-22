from app.extensions import db
from . import BaseModel

# Many-to-Many relationship table
place_amenities = db.Table(
    'place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey(
        'places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey(
        'amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)

    amenities = db.relationship(
        'Amenity', secondary='place_amenities', backref='places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
