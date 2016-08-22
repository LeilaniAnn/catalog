from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
User1 = User(name="Leilani Raranga", email="retrosole@gmail.com",
             picture='http://my.xfinity.com/blogs/tv/files/2010/08/Dora.jpg')
session.add(User1)
session.commit()


# category1 = Category(name="Lipstick")
# session.add(category1)
# session.commit()
# category2 = Category(name="Mascara")
# session.add(category2)
# session.commit()
# category3 = Category(name="Eyeshadow")
# session.add(category3)
# session.commit()
# category4 = Category(name="Foundation")
# session.add(category4)
# session.commit()

# Item1 = Item(name="Burbery Kisses Lipstick",
#              description="Nude Beige No. 01 - Pale beige",
#              price="$33.00",
#              image="http://www.sephora.com/productimages/sku/s1740489-main-Lhero.jpg",
#              category=category1)

# session.add(Item1)
# session.commit()

# Item2 = Item(name="Yves Saint Laurent Rouge Pur Couture Star Clash Edition",
#              description="52 Rouge Rose",
#              price="$37.00",
#              image="http://www.sephora.com/productimages/sku/s1863257-main-Lhero.jpg",
#              category=category1)

# session.add(Item2)
# session.commit()

# Item3 = Item(name="MUF Ultra HD Invisible Cover Foundation",
#              description="A bestselling HD foundation with an ultra lightweight texture that provides ultra flawless skin.",
#              price="$43.00",
#              image="http://www.sephora.com/productimages/sku/s1708957-main-Lhero.jpg",
#              category=category4)

# session.add(Item3)
# session.commit()

# Item4 = Item(name="Benefit Cosmetics They're Real! Mascara",
#              description="A lengthening mascara that curls and separates lashes for an out of here look now available in three vibrant shades.",
#              price="$24.00",
#              image="http://www.sephora.com/productimages/sku/s1343938-main-Lhero.jpg",
#              category=category2)

# session.add(Item4)
# session.commit()

# Item5 = Item(name="Marc Jacobs Beauty Style Eye Con No 20 Eyeshadow Palette",
#              description="A limited-edition palette of 20 plush eye shadows in luxurious finishes, organized in five columns, for a complete wardrobe of looks. ",
#              price="$99.00",
#              image="hhttp://www.sephora.com/productimages/sku/s1838150-main-Lhero.jpg",
#              category=category3)

# session.add(Item5)
# session.commit()
print "added new items!"
