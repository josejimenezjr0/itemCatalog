from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100))
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    # item = relationship(Item)

class Category(Base):
    __tablename__ = 'category'

    name = Column(String(100),unique=True, nullable=False)
    id = Column(Integer, primary_key=True)
    # item = relationship(Item)

class Item(Base):
    __tablename__ = 'item'
    name = Column(String(100), unique=True, nullable=True)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    category_id = Column(Integer, ForeignKey('category.id'))

dbString = 'postgresql://postgres:postgres@127.0.0.1:5432/itemCatalog'
engine = create_engine(dbString)
Base.metadata.create_all(engine)