from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return pwd_context.hash(password)

def verify(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass,hashed_pass)