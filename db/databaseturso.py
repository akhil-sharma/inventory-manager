from .datainterface import DataInterface
from models import InventoryInDB, InventoryItem, ItemInDB, UserOut, UserInDB
import libsql_client
from libsql_client import ClientSync, ResultSet
from decouple import config

class DatabaseTurso(DataInterface):
       
    def _get_client(self) -> ClientSync:
        url = config("DATABASE_URL")
        auth_token = config("AUTH_TOKEN")
        
        if not url:
            raise Exception("INVALID DATABASE URL. PLEASE CHECK YOUR \'.ini FILE\'.")
        
        if not auth_token:
            print("Trying to connect without the auth token")
        
        try:
            client = libsql_client.create_client_sync(url=url, auth_token=auth_token)
            return client
        except Exception as e:
            print("Unable to connect with the database. Check connection details.")
            raise
        
    def get_user_from_id(self, id: str) -> UserInDB:
        client = None
        try:
            client = self._get_client()
            
            resultSet = client.execute(
                "SELECT user_id, first_name, last_name, email, password_hash FROM tb_users where user_id = ?",
                [id]
            )
            
            if len(resultSet) == 0:
                raise Exception("User not found.")
            
            return UserInDB(
                first_name=resultSet[0]["first_name"],
                last_name=resultSet[0]["last_name"],
                email=resultSet[0]["email"],
                password_hash=resultSet[0]["password_hash"]
            )     
        
        except Exception as e:
            print("error in get_user_from_id...")
            print(e)
        
        finally:
            client.close()
            
    def get_user_from_email(self, email) -> UserInDB:
        client = None
        try:
            client = self._get_client()
            
            resultSet = client.execute(
                "SELECT user_id, first_name, last_name, email, password_hash FROM tb_users where email = ?",
                [email]
            )
            
            if len(resultSet) == 0:
                raise Exception("User not found.")
            
            print("Done 1")
            return UserInDB(
                user_id=resultSet[0]["user_id"],
                first_name=resultSet[0]["first_name"],
                last_name=resultSet[0]["last_name"],
                email=resultSet[0]["email"],
                password_hash=resultSet[0]["password_hash"]
            )     
        
        except Exception as e:
            print("error in get_user_from_email...")
            print(e)
        
        finally:
            client.close()

    def create_user(self, user: UserInDB) -> UserOut:
        client = None
        try:
            client = self._get_client()
            
            ResultSet = client.execute(
                """INSERT INTO tb_users (user_id, first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?, ?)""",
                [user.user_id, user.first_name, user.last_name, user.email, user.password_hash]
            )
            
            if ResultSet.rows_affected != 1:
                raise Exception("Error when inserting data into tb_users.")
            
            return user
            
        except Exception as e:
            print("error in create_user.")
            print(e)
        
        finally:
            client.close()

    def create_inventory(self, inventory: InventoryInDB) -> InventoryInDB:
        client = None
        try:
            client = self._get_client()
            ResultSet = client.execute(
                """INSERT INTO tb_inventory (inventory_id, inventory_name, user_id, description) VALUES (?, ?, ?, ?)""",
                [inventory.inventory_id, inventory.inventory_name, inventory.user_id, inventory.description]
            )

            if ResultSet.rows_affected != 1:
                raise Exception("Error when inserting data into tb_inventory.")
            
            return inventory
        
        except Exception as e:
            print("error in create_inventory.")
            print(e)
        
        finally:
            client.close()

    def get_inventory_from_id(self, inventory_id: str, user_id: str) -> InventoryInDB:
        client = None
        try:
            client = self._get_client()
            
            resultSet = client.execute(
                "SELECT inventory_id, inventory_name, user_id, description FROM tb_inventory WHERE inventory_id = ? AND user_id = ?",
                [user_id, inventory_id]
            )
            
            if len(resultSet) == 0:
                raise Exception("Inventory not found.")
            
            return InventoryInDB(
                inventory_id=resultSet[0]["inventory_id"],
                inventory_name=resultSet[0]["inventory_name"],
                user_id=resultSet[0]["user_id"],
                description=resultSet[0]["description"]
            )     
        
        except Exception as e:
            print("error in get_inventory_from_id...")
            print(e)
        
        finally:
            client.close()

    def get_inventory_from_name(self, inventory_name: str, user_id: str) -> InventoryInDB:
        client = None
        try:
            client = self._get_client()
            
            resultSet = client.execute(
                "SELECT inventory_id, inventory_name, user_id, description FROM tb_inventory where inventory_name = ? AND user_id = ?",
                [inventory_name, user_id]
            )
            
            if len(resultSet) == 0:
                raise Exception("Inventory not found.")
            
            return InventoryInDB(
                inventory_id=resultSet[0]["inventory_id"],
                inventory_name=resultSet[0]["inventory_name"],
                user_id=resultSet[0]["user_id"],
                description=resultSet[0]["description"]
            )     
        
        except Exception as e:
            print("error in get_inventory_from_name...")
            print(e)
        
        finally:
            client.close()
    
    def create_item(self, item: ItemInDB) -> ItemInDB:
        client = None
        try:
            client = self._get_client()
            ResultSet = client.execute(
                """INSERT INTO tb_items (item_id, item_name, user_id) VALUES (?, ?, ?)""",
                [item.item_id, item.item_name, item.user_id]
            )

            if ResultSet.rows_affected != 1:
                raise Exception("Error when inserting data into tb_item.")
            
            return item
        
        except Exception as e:
            print("error in create_item.")
            print(e)

        finally:
            client.close()

    def get_item_from_id(self, item_id: str, user_id: str) -> ItemInDB:
        client = None
        try:
            client = self._get_client()
            
            resultSet = client.execute(
                "SELECT item_id, item_name, user_id FROM tb_items where item_id = ? AND user_id = ?",
                [item_id, user_id]
            )
            
            if len(resultSet) == 0:
                raise Exception("Item not found.")
            
            return InventoryInDB(
                item_id=resultSet[0]["item_id"],
                item_name=resultSet[0]["item_name"],
                user_id=resultSet[0]["user_id"],
            )     
        
        except Exception as e:
            print("error in get_item_from_id...")
            print(e)
        
        finally:
            client.close()

    def get_item_from_name(self, item_name: str, user_id: str) -> ItemInDB:
        client = None
        try:
            client = self._get_client()
            
            resultSet = client.execute(
                "SELECT item_id, item_name, user_id FROM tb_items where item_name = ? AND user_id = ?",
                [item_name, user_id]
            )
            
            if len(resultSet) == 0:
                raise Exception("Item not found.")
            
            return ItemInDB(
                item_id=resultSet[0]["item_id"],
                item_name=resultSet[0]["item_name"],
                user_id=resultSet[0]["user_id"],
            )     
        
        except Exception as e:
            print("error in get_item_from_name...")
            print(e)
        
        finally:
            client.close()

    def add_item_to_inventory(self, inventory_item :InventoryItem) -> InventoryItem:
        client = None
        try:
            client = self._get_client()
            ResultSet = client.execute(
                """INSERT INTO tb_inventory_items (item_id, inventory_id, user_id) VALUES (?, ?, ?)""",
                [inventory_item.item_id, inventory_item.inventory_id, inventory_item.user_id]
            )

            if ResultSet.rows_affected != 1:
                raise Exception("Error when inserting data into tb_item.")
            
            return inventory_item
        
        except Exception as e:
            print("error in add_item_to_inventory.")
            print(e)
        
        finally:
            client.close()

    def get_inventory_item(self, inventory_item: InventoryItem) -> InventoryItem:
        client = None
        try:
            client = self._get_client()
            
            resultSet = client.execute(
                "SELECT inventory_id, item_id, user_id FROM tb_inventory_items where inventory_id = ? AND item_id = ? AND user_id = ?",
                [inventory_item.inventory_id, inventory_item.item_id, inventory_item.user_id]
            )
            
            if len(resultSet) == 0:
                raise Exception("Item not in inventory.")
            
            return InventoryItem(
                inventory_id=resultSet[0]["inventory_id"],
                item_id=resultSet[0]["item_id"],
                user_id=resultSet[0]["user_id"],
            )     
        
        except Exception as e:
            print("error in get_inventory_item...")
            print(e)
        
        finally:
            client.close()
