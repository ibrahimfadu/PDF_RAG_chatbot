from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column


class User(Base):
    __table_name__ = "User"
    name:Mapped[str] = mapped_column(String(255))
    email: Mapped[str] 
    user: Mapped[str] = mapped_column(primary_key=true)
    hashed_password: Mapped[str] 

