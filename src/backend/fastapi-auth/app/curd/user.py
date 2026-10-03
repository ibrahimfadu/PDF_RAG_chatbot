from sqlalchemy.orm import Session 
from app.models.user import User
form app.schemas.user import UserCreate,UserLogin,UserRead



def create_user(db: Session,data: UserCreate):
    user = User(
        name = data.name,
        email = data.email,
        password = data.password
    ) 
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

