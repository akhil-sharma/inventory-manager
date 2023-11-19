from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from decouple import config
import uuid

from db.databaseturso import DatabaseTurso
from models import UserOut, UserIn, UserInDB, TokenData, Token, InventoryInDB, InventoryIn, ItemIn, ItemInDB, InventoryItem

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
database = DatabaseTurso()

# Dependencies

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

def create_inventory_service(inventory_in: InventoryIn, user_id: str) -> InventoryInDB:
    existing_inventory = database.get_inventory_from_name(inventory_in.inventory_name, user_id)
    if existing_inventory:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An inventory with the same name already exists."
        )
    
    inventory_id = uuid.uuid4().hex
    inventory_in_database = InventoryInDB(
        inventory_name=inventory_in.inventory_name,
        description=inventory_in.description,
        inventory_id=inventory_id,
        user_id=user_id
    )
    
    return database.create_inventory(inventory_in_database)

def create_item_service(item_in: ItemIn, user_id: str) -> ItemInDB:
    existing_item = database.get_item_from_name(item_in.item_name, user_id)
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An item with the same name already exists."
        )
    
    item_id = uuid.uuid4().hex
    item_in_database = ItemInDB(
        item_name=item_in.item_name,
        item_id=item_id,
        user_id=user_id
    )
    
    return database.create_item(item_in_database)

# Paths

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
    

@app.get("/users/me", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    return current_user

@app.post("/inventories/", response_model=InventoryInDB)
async def create_inventory(
    inventory_in: InventoryIn, current_user: Annotated[UserOut, Depends(get_current_user)]
):
    return create_inventory_service(inventory_in, current_user.user_id)


@app.post("/items/", response_model=ItemInDB)
async def create_item(
    item_in: ItemIn, current_user: Annotated[UserOut, Depends(get_current_user)]
):
    return create_item_service(item_in, current_user.user_id)

@app.post("/inventories/{inventory_name}/items", response_model=List[InventoryItem])
async def add_items_to_inventory(
    inventory_name: str, items: List[ItemIn], current_user: Annotated[UserOut, Depends(get_current_user)]
):
    existing_inventory = database.get_inventory_from_name(inventory_name, current_user.user_id)
    if not existing_inventory:
        inventory_in = InventoryIn(inventory_name=inventory_name)
        existing_inventory = create_inventory_service(inventory_in, current_user.user_id)

    added_inventory_items = []

    for item_in in items:
        existing_item = database.get_item_from_name(item_in.item_name, current_user.user_id)
        if not existing_item:
            existing_item = create_item_service(item_in, current_user.user_id)

        inventory_item_data = InventoryItem(
            item_id=existing_item.item_id,
            inventory_id=existing_inventory.inventory_id,
            user_id=current_user.user_id
        )
        
        existing_item_in_inventory = database.get_inventory_item(inventory_item_data)
        if not existing_item_in_inventory:
            print(item_in.item_name)
            added_item = database.add_item_to_inventory(inventory_item_data)
            if not added_item:
                continue  # continue processing rest of the items.
            added_inventory_items.append(added_item)

    return added_inventory_items
