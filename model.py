# import requests
# import yelpapi
# from yelpapi import YelpAPI
import pprint
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User of travel map webapp"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
    
        return "<User user_name=%s fname=%s lname=%s email=%s >" % (self.user_name, self.fname, self.lname, self.email)


class Folder(db.Model):
    """Folder table for each user"""

    __tablename__ = "folders"
    
    folder_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    folder_name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
    
        return "<Folder folder_name=%s user=%s >" % (self.folder_name, self.user_id)

    def to_dict(self):
        return {
            'id': self.folder_id,
            'name': self.folder_name,
            'user_id': self.user_id,
        }


class Place(db.Model):
    """Table for places saved in the folder"""

    __tablename__ = "places"

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
    
        return "<Place category=%s name=%s address=%s >" % (self.category, self.name, self.address)


class Place_folder(db.Model):
    """Association table for places and folders tables"""

    __tablename__ = "places_folders"

    place_folder_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.place_id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'), nullable=False)

    def __repr__(self):

        return "<Association table id=%s>" % (self.id)

# Helper functions
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placesquery.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
