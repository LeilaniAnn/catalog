from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from db import Base, Category, Item
 
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



category1 = Category(name = "Lipstick")
session.add(category1)
session.commit()
category2 = Category(name = "Mascara")
session.add(category2)
session.commit()
category3 = Category(name = "Eyeshadow")
session.add(category3)
session.commit()

Item1 = Item(name = "Burbery Kisses Lipstick", 
			 description = "Nude Beige No. 01 - Pale beige", 
			 price = "$33.00", 
			 image = "http://www.sephora.com/productimages/sku/s1740489-main-Lhero.jpg", 
			 category = category1)

session.add(Item1)
session.commit()

Item2 = Item(name = "Yves Saint Laurent Rouge Pur Couture Star Clash Edition", 
			 description = "52 Rouge Rose", 
			 price = "$37.00", 
			 image = "http://www.sephora.com/productimages/sku/s1863257-main-Lhero.jpg", 
			 category = category1)

session.add(Item2)
session.commit()
print "added new items!"
