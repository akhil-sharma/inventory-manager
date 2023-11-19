from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    user_id: str

class UserInDB(UserBase):
    user_id: str
    password_hash: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_Id: str | None = None

class InventoryBase(BaseModel):
    inventory_name: str
    description: str | None = None

class InventoryIn(InventoryBase):
    pass

class InventoryInDB(InventoryBase):
    inventory_id: str
    user_id: str

class ItemBase(BaseModel):
    item_name: str

class ItemIn(ItemBase):
    pass

class ItemInDB(ItemBase):
    item_id: str
    user_id: str

class InventoryItem(BaseModel):
    item_id: str
    inventory_id: str
    user_id: str
