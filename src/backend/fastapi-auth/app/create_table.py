from app.database imoprt Base,engine
from app.models import User

    
def create_table():
    Bind.metabata.create_all(bind=engine)


if __name__=="__main__":
    create_table();

