from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise credentials_exception
    

def get_current_borrower(current_user=Depends(get_current_user)):
    if current_user["role"] != "borrower":
        raise HTTPException(
            status_code=403,
            detail="Borrower access only"
        )
    return current_user


def get_current_lender(current_user=Depends(get_current_user)):
    if current_user["role"] != "lender":
        raise HTTPException(
            status_code=403,
            detail="Lender access only"
        )
    return current_user