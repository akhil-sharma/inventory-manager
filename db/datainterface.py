from abc import ABC, abstractmethod
from models import UserIn, UserOut, UserInDB, InventoryIn, InventoryInDB, InventoryItem, ItemIn, ItemInDB

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

    @abstractmethod
    def create_inventory(self, inventory: InventoryIn) -> InventoryInDB:
        pass

    @abstractmethod
    def get_inventory_from_id(self, inventory_id: str, user_id: str) -> InventoryInDB:
        pass

    @abstractmethod
    def get_inventory_from_name(self, inventory_name: str, user_id: str) -> InventoryInDB:
        pass

    @abstractmethod
    def create_item(self, item: ItemIn) -> ItemInDB:
        pass

    @abstractmethod
    def get_item_from_id(self, item_id: str, user_id: str) -> ItemInDB:
        pass

    @abstractmethod
    def get_item_from_name(self, item_name: str, user_id: str) -> ItemInDB:
        pass

    @abstractmethod
    def add_item_to_inventory(self, inventory_item: InventoryItem) -> InventoryItem:
        pass

    @abstractmethod
    def get_inventory_item(self, inventory_item: InventoryItem) -> InventoryItem:
        pass
