from fastapi import Depends,FastAPI
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


@app.get("/items/")
async def home(token: Annotated[str,Depends(oauth2)]):
    return {"token":token}
    

