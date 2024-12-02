from sqlalchemy import Column,Integer,String
from database import Base

class Item(Base):
   __tablename__ = 'users'

   id = Column(Integer, primary_key=True)
   title = Column(String, index=True)
   description = Column(String, index=True)
   price = Column(Integer)
