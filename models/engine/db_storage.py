#!/user/bin/python3
""" This module defines a class to manage db storage for hbnb clone"""

from sqlalchemy import (create_engine)
import os
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """SQL database storage """

    __engine = None
    __session = None
    classes = {
               'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }

    def __init__(self):
        """ Create engine and connect to database"""

        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        db = os.getenv('HBNB_MYSQL_DB')
        host = os.getenv('HBNB_MYSQL_HOST')
        envv = os.getenv('HBNB_ENV', 'none')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of __objects """

        dic = {}

        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            print("start")
            for obj in query:
                dic[obj.__class__.__name__ + "." + obj.id] = obj
        else:
            for c in self.classes.values():
                query = self.__session.query(c)
                for obj in query:
                    dic[obj.__class__.__name__ + "." + obj.id] = obj

        return (dic)

    def new(self, obj):
        """ add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete()

    def reload(self):
        """
        create current database session from the engine
        using a sessionmaker
        """

        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def  close(self):
        """ close the dbstorage"""
        self.__session.close()
