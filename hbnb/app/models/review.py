from app.extensions import db
from . import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey(
        'places.id'), nullable=False)

    def __init__(self, text, rating, user_id, place_id):
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
