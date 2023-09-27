from fastapi import APIRouter
from ..models import NewUser

'''
This router is dedicated for managing the users.
This may include creating/deleting users, updating
profiles etc.
'''

router = APIRouter()

@router.get("/user/{user_id}", tags=["users"])
def get_user(user_id: str):
    '''
    Returns the user details.
    **The user_id should be retrieves from a middleware.**
    '''
    return {"user_id": user_id}

@router.post("/user/", tags=["users"])
def create_user(user: NewUser):
    '''
    Creates a new user and returns the User object
    While also setting a httpOnly cookie for auth.
        1. Check that the email does not exists.
        2. hash the password
        2. Insert the user.
        3. Return the user details.
    '''
    return user