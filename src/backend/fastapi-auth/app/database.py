from sqlalchemy import create_engine
from app.config import get_setting 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

setting = get_setting()

engine = create_engine(setting.DATABASE_URL)

LocalSession = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close();

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())




