from sqlalchemy import Table, Column, Integer, String, MetaData
from database import Base

class Cat(Base):
    __tablename__= "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    age = Column(Integer)

