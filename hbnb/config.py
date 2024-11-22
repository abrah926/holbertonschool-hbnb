import os


class Config:
    SECRET_KEY = "ac201e0ec31643e33c7d77de693c62e866715875dc83b5a008203d8e3d5fe787"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Keep JWT consistent across environments
    JWT_SECRET_KEY = '830b5265c119474d963c640623e9e41a'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Micasa#1758926@localhost/hbnb_dev'
    DEBUG = True  # Enable debug mode for development


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Micasa#1758926@localhost/hbnb_dev'
    DEBUG = False  # Disable debug mode for production
