from fastapi import Depends,status,HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from .config import settings



#This line means:
# FastAPI expects the user to send token using Authorization: Bearer <token>
# “Hey, expect the client to send the token in this format: Authorization: Bearer <token>”
# tokenUrl='login' tells Swagger where the token is generated (your login route)
# #That’s why “Authorize” button in Swagger magically works.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



# This is what you call in your login route to generate a token.
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#verify_access_token() — Used by protected routes
#Purpose: This function validates the token and extracts user info.
#If someone tampers with the token? Expired? Wrong signature? → 🔥 401 Unauthorized!

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode JWT
        id: str = payload.get("user_id")  # Extract user_id

        if id is None:
            raise credentials_exception  # If ID not present in token

        token_data = schemas.TokenData(id=id)  # Pydantic validation (optional but clean)
        return token_data  # ✅ Return token data

    except JWTError:
        raise credentials_exception  # If token is invalid/expired



 #This function:
#   Is used as a dependency for protected routes
#   Automatically pulls the token from Authorization header
#   Verifies the token and gets the user ID


def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}  # <- spelling fixed here!
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id==token_data.id).first()
    return user  # return just the ID

