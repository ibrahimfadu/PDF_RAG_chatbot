from sqlalchemy import Column,Integer,String,Boolean,DateTime
from app.database import Base

class User(Base):
    __table_name__ = "user"
    id = Column(Integer,primary_key = True)
    name = Column(String)
    email = Column(String,unique = True,nullable = False)
    password = Column(String)






