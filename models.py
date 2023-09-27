from pydantic import BaseModel

class NewUser(BaseModel):
    '''
    This model is used when the information about the user is first received.
    '''
    first_name: str
    last_name: str
    email: str
    password: str

class User(BaseModel):
    '''
    For regular work the user model does not require the password key.
    '''
    first_name: str
    last_name: str
    email: str
