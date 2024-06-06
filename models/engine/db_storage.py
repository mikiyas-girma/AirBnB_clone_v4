#!/usr/bin/python3
"""
this module contains an engine to connect and
ables us to talk with the mysql database
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity


class DBStorage:
    """dbstorage engine's class used for creating the db engine, session
    and managing the database storage and operations on it
    """
    __engine = None
    __session = None

    def __init__(self):
        """creates the database engine and prepares the working
        environment initially"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}"
            .format(getenv("HBNB_MYSQL_USER"),
                    getenv("HBNB_MYSQL_PWD"),
                    getenv("HBNB_MYSQL_HOST"),
                    getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session
        and returns a dictionary of models"""
        classes = [State, User, City, Amenity, Place, Review]
        obj_dict = {}
        if cls is None:
            for cls in classes:
                query = self.__session.query(cls)
                for obj in query.a():
                    key = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                key = obj.__class__.__name__ + '.' + obj.id
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """adds the obj passed to database storage"""
        if not obj:
            return
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes the passed object from the database"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """ calls remove() method on the private session attribute"""
        self.__session.close()

    def get(self, cls, id):
        '''
        gets an object
        '''
        obj_dict = models.storage.all(cls)
        for k, v in obj_dict.items():
            matchstring = cls.__name__ + '.' + id
            if k == matchstring:
                return v

        return None

    def count(self, cls=None):
        '''
        counts number of objects of a class (if given)
        '''
        obj_dict = models.storage.all(cls)
        return len(obj_dict)
