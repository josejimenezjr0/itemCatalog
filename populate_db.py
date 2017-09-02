#!/usr/bin/env python
"""
Populates the database with initial categories and items
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Category, Item, Base

#Setup datbase connections
dbString = 'postgresql://catalog:grader@127.0.0.1:5432/itemcatalog'
engine = create_engine(dbString)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Robot", email="robot@robot.com")
session.add(User1)
session.commit()

# Category for Football
category1 = Category(name='Football')

session.add(category1)
session.commit()

#Items for Football
desc = [
    'A padded helmet with a',
    ' face mask to protect the head of football players'
    ]

item = Item(
    name='Helmet',
    description=''.join(desc),
    category=category1,
    user_id=1)

session.add(item)
session.commit()

desc = [
    'An inflated oval with a bladder contained',
    ' in a casing usually made of leather.'
    ]

item = Item(
    name='Football',
    description=''.join(desc),
    category=category1,
    user_id=1)

session.add(item)
session.commit()

item = Item(
    name='Cleats',
    description='A shoe fitted with conical projections.',
    category=category1,
    user_id=1)

session.add(item)
session.commit()

# Category for Baseball
category1 = Category(name='Baseball')

session.add(category1)
session.commit()

#items for Baseball
desc = [
    'A sphere 3 inches in diameter with cork ',
    'center covered by stitched horsehide.'
    ]

item = Item(
    name='Baseball',
    description=''.join(desc),
    category=category1,
    user_id=1)

session.add(item)
session.commit()

item = Item(
    name='Glove',
    description='Padded covering for hand with a pocket to catch baseballs.',
    category=category1,
    user_id=1)

session.add(item)
session.commit()

item = Item(
    name='Bat',
    description='The wooden club used to strike the ball',
    category=category1,
    user_id=1)

session.add(item)
session.commit()

# Category for Hockey
category1 = Category(name='Hockey')

session.add(category1)
session.commit()

#items for Hockey
item = Item(
    name='Puck',
    description='A black disk of vulcanized rubber.',
    category=category1,
    user_id=1)

session.add(item)
session.commit()

item = Item(
    name="Stick",
    description='The stick used in field hockey or ice hockey',
    category=category1,
    user_id=1)

session.add(item)
session.commit()

desc = [
    'a nylon netting structure attached to ',
    'goalposts and skirting around the base.'
]

item = Item(
    name="Net",
    description=''.join(desc),
    category=category1,
    user_id=1)

session.add(item)
session.commit()

print "added categories and items!"
