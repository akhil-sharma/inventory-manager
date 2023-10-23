from abc import ABC, abstractmethod
from models import UserIn, UserOut, UserInDB

class DataInterface(ABC):
    
    @abstractmethod
    def get_user_from_id(self, id: str) -> UserInDB:
        pass
    
    @abstractmethod
    def get_user_from_email(self, email: str) -> UserInDB:
        pass

    @abstractmethod
    def create_user(self, user: UserIn) -> UserOut:
        pass
