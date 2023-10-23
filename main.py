from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from decouple import config
import uuid

from db.databaseturso import DatabaseTurso
from models import UserOut, UserIn, UserInDB, TokenData, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
database = DatabaseTurso()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    '''
    The username string used for login is simply the email address.
    '''
    user = database.get_user_from_email(username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config("SECRET_KEY"), algorithm=config("ALGORITHM"))
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, config("SECRET_KEY"), algorithms=[config("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = database.get_user_from_email(username)
    if user is None:
        raise credentials_exception
    return user    


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_toke_expires = timedelta(minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_toke_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=UserOut)
async def register_new_user(userDetail: UserIn):
    existing_user = database.get_user_from_email(userDetail.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The username already exists."
        )
    user_id = uuid.uuid4().hex
    password_hash = get_password_hash(userDetail.password)
    user_in_database = UserInDB(
        user_id=user_id,
        first_name=userDetail.first_name,
        last_name=userDetail.last_name,
        email=userDetail.email,
        password_hash=password_hash
    )
    newUser = database.create_user(user_in_database)
    if not newUser:
        raise
    
    return newUser
    

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    return current_user