from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Category, Item, Base

dbString = 'postgresql://postgres:postgres@127.0.0.1:5432/itemCatalog'
engine = create_engine(dbString)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Category for Football
category1 = Category(name='Football')

session.add(category1)
session.commit()

desc = ("""
A padded helmet with a face mask to protect the head of football players
""")

item = Item(
    name='Helmet',
    description=desc,
    category=category1)

session.add(item)
session.commit()

desc = ("""
An inflated oval with a bladder contained in a casing usually made of leather.
""")

item = Item(
    name='Football',
    description=desc,
    category=category1)

session.add(item)
session.commit()

item = Item(
    name='Cleats',
    description='A shoe fitted with conical projections.',
    category=category1)

session.add(item)
session.commit()

# Category for Baseball
category1 = Category(name='Baseball')

session.add(category1)
session.commit()

desc = ("""
A sphere 3 inches in diameter with cork center covered by stitched horsehide.
""")

item = Item(
    name='Baseball',
    description=desc,
    category=category1)

session.add(item)
session.commit()

item = Item(
    name='Glove',
    description='Padded covering for hand with a pocket to catch baseballs.',
    category=category1)

session.add(item)
session.commit()

item = Item(
    name='Bat',
    description='The wooden club used to strike the ball',
    category=category1)

session.add(item)
session.commit()

# Category for Hockey
category1 = Category(name='Hockey')

session.add(category1)
session.commit()

item = Item(
    name='Puck',
    description='A black disk of vulcanized rubber.',
    category=category1)

session.add(item)
session.commit()

item = Item(
    name="Stick",
    description='The stick used in field hockey or ice hockey',
    category=category1)

session.add(item)
session.commit()

desc = ("""
a nylon netting structure attached to goalposts and skirting around the base.
""")

item = Item(
    name="Net",
    description=desc,
    category=category1)

session.add(item)
session.commit()

print "added categories and items!"