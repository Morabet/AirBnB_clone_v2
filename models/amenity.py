#!/usr/bin/python3
""" Amenity Module for HBNB project """

import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Represents an Amenity for a MySQL database"""
    __tablename__ = 'amenities'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place',
                                       secondary="place_amenity",
                                       back_populates="amenities")

    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """ Instatntiates Amenity"""
        super().__init__(*args, **kwargs)
