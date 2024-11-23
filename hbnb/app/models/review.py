from app.extensions import db
import uuid
from . import BaseModel
from app.models.user import User


class Review(BaseModel):
    __tablename__ = 'reviews'
    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_check'),
    )
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey(
        'places.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))

    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.user_id = user_id  # Store user_id directly
        self.place_id = place_id  # Store place_id directly

    def _validate_text(self, text):
        """Validate the text of the review."""
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if len(text) > 128:
            raise ValueError("Review text must be 128 characters or less")
        return text

    def _validate_rating(self, rating):
        """Validate the rating of the review."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating
