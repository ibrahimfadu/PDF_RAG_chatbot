from sqlalchemy import create_engine
from config import get_setting 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
setting = get_setting()

engin = create_engine(setting.DATABASE_URL)

LocalSession = sessionmaker(bind=engine)
Base = declarative_base


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close();




