from app.core.database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__ = "User"
    id = Column(Integer,primary_key = True)
    Fname = Column(String(50))
    Lname = Column(String(100))
    email = Column(String(70),unique=True)

