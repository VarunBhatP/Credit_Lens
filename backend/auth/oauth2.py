from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise credentials_exception

def get_current_borrower(current_user=Depends(get_current_user)):
    if current_user["role"] != "borrower":
        raise HTTPException(status_code=403, detail="Borrower access only")
    return current_user

def get_current_lender(current_user=Depends(get_current_user)):
    if current_user["role"] != "lender":
        raise HTTPException(status_code=403, detail="Lender access only")
    return current_user