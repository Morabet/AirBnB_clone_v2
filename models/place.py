#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review


place_amenity = Table(
        "place_amenity", Base.metadata,
        Column('place_id', String(60),
               ForeignKey("places.id"),
               primary_key=True),
        Column('amenity_id', String(60),
               ForeignKey("amenities.id"),
               primary_key=True)
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship('Review',
                               backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship('Amenity',
                                 secondary="place_amenity",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Getter for the Review """
            from models import storage
            review_list = []
            review_dict = stroge.all(Review).values()
            for obj in review_dict:
                if obj.place_id == self.id:
                    review_list.append(obj)

            return review_list

        @property
        def amenities(self):
            """Getter for the Amenity """
            from models import storage
            amenities_list = []
            amenities_dict = stroge.all(Amenity).values()
            for ame in amenities_dict:
                if ame.id in self.amenity_ids:
                    amenities_list.append(ame)

            return amenities_list

        @amenities.setter
        def amenities(self, value):
            """ setter for the amenity """
            if type(value).__name__ == "Amenity":
                self.amenity_ids.append(value.id)
