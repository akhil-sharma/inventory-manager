from .datainterface import DataInterface
from models import UserOut, UserInDB
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

