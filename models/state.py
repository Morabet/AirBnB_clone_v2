#!/usr/bin/python3

""" State Module for HBNB project """

import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)
        cities = relationship('City',
                              backref="state",
                              cascade="all, delete-orphan")

    else:
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """Getter for the City """
            from models import storage
            city_list = []
            city_dict = stroge.all(self).values()
            for obj in city_dict:
                if obj.state_id == self.id:
                    city_list.append(obj)

            return city_list
