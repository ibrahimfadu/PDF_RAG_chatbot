from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlaalchem.ext.declarative import declarative_base

SQLALCHEMY_DATABASE = "postgres//user:password@localhost:5423/postgres"

engine = create_engine(SQLALCHEMY_DATABASE)

LocalSession = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield
    finally:
        db.close()




