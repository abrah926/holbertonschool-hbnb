from abc import ABC, abstractmethod
from app.extensions import db
# Assuming SQLAlchemy is initialized in app.extensions


# Abstract Base Repository
class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


# In-Memory Repository Implementation
class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


# SQLAlchemy Repository Implementation
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address.
        """
        return self.get_by_attribute('email', email)


# Specialized Repositories
class UserRepository(InMemoryRepository):  # For in-memory usage
    def __init__(self):
        super().__init__()

    def get_by_attribute(self, attr_name, attr_value):
        return next((user for user in self._storage.values() if getattr(user, attr_name) == attr_value), None)


class SQLAlchemyUserRepository(SQLAlchemyRepository):  # For database usage
    def __init__(self):
        from app.models import User  # Import your SQLAlchemy User model here
        super().__init__(User)


class PlaceRepository(InMemoryRepository):  # For in-memory usage
    def __init__(self):
        super().__init__()


class SQLAlchemyPlaceRepository(SQLAlchemyRepository):  # For database usage
    def __init__(self):
        from app.models import Place  # Import your SQLAlchemy Place model here
        super().__init__(Place)


class ReviewRepository(InMemoryRepository):  # For in-memory usage
    def __init__(self):
        super().__init__()


class SQLAlchemyReviewRepository(SQLAlchemyRepository):  # For database usage
    def __init__(self):
        from app.models import Review  # Import your SQLAlchemy Review model here
        super().__init__(Review)


class AmenityRepository(InMemoryRepository):  # For in-memory usage
    def __init__(self):
        super().__init__()


class SQLAlchemyAmenityRepository(SQLAlchemyRepository):  # For database usage
    def __init__(self):
        from app.models import Amenity  # Import your SQLAlchemy Amenity model here
        super().__init__(Amenity)
