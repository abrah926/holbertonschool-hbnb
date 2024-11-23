from app.extensions import db
import uuid
from . import BaseModel
from app.models.user import User


class Review(BaseModel):
    __tablename__ = 'reviews'
    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_check'),
    )

    text = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey(
        'places.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __init__(self, text, rating, user, place):
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.user = self._validate_user(user)
        self.place = self._validate_place(place)
        self.user_id = user.id
        self.place_id = place.id
