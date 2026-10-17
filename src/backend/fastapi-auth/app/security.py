import bcrypt 

def hash_password(plan: str) -> str:
    return bcrypt.hashpw(plan.encode(),bcrypt.gensalt()).decode()

def verify_password(plan: str,hashed : str)->str:
    return bcrypt.checkpw(plain.encode(), hashed.encode())
