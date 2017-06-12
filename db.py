from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    Items = relationship("Item", cascade = "all, delete-orphan")

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class Item(Base):
    __tablename__ = 'item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    image = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
           'price'        : self.price,
           'image'        : self.image,
       }



engine = create_engine('postgres://yrxpfopslthutl:bc54417c098ea15e644d863a3d7c6ef2c8710d239c472dda5ae1c793eccbdc0d@ec2-50-19-219-69.compute-1.amazonaws.com:5432/d1hnt7dov574q5')
 

Base.metadata.create_all(engine)
