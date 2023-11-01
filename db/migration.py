"""
    **DANGEROUS**
    
    This files resets the remote database
    deleting all tables and recreating them.
    
    This will effect all developers working on
    or testing the application.
"""

import libsql_client
from decouple import config
import uuid

client = libsql_client.create_client_sync(
    url=config("DATABASE_URL"),
    auth_token=config("AUTH_TOKEN")
    )

try:
    
    client.batch([
        libsql_client.Statement("DROP TABLE IF EXISTS tb_inventory_items"),
        
        libsql_client.Statement("DROP TABLE IF EXISTS tb_items"),
        
        libsql_client.Statement("DROP TABLE IF EXISTS tb_inventory"),
        
        libsql_client.Statement("DROP TABLE IF EXISTS tb_users")        
        
    ])
    
    client.batch([
        # tb_users
        
        
        libsql_client.Statement(
            """CREATE TABLE tb_users (
                    user_id varchar(32) PRIMARY KEY,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255)
                    )"""
        ),
        
        libsql_client.Statement("""INSERT INTO tb_users (user_id, first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?, ?)""", 
            ["1e92ff25cd3245f3920672295ae8c8b7", "a", "b", "a@bc.com", "$2b$12$a.eOTvR2O3plDFLoF5atXubx49XZE6dz1ghuztINDxOY7Feon.inm"])
    ])

    rs = client.execute("SELECT * FROM tb_users")

    if len(rs) > 0:
        print("The following data has been added: \n")
        for row in rs:
            print(row)
    
    ##############################################
    
    client.batch([
        # tb_inventory
        
        
        libsql_client.Statement(
            """CREATE TABLE tb_inventory (
                    inventory_id varchar(32) PRIMARY KEY,
                    inventory_name VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    description VARCHAR(255),
                    FOREIGN KEY(user_id) REFERENCES tb_users(user_id)
                    )"""
        ),
        
        libsql_client.Statement("""INSERT INTO tb_inventory (inventory_id, inventory_name, user_id, description) VALUES (?, ?, ?, ?)""", 
            ["a9504954a98c4b71bfe6e032b8e40ab1", "sample-1", "1e92ff25cd3245f3920672295ae8c8b7", "A sample inventory created by akhil"])
    
    ])

    rs = client.execute("SELECT * FROM tb_inventory")

    if len(rs) > 0:
        print("The following data has been added: \n")
        for row in rs:
            print(row)
            
    #############################################
    
    client.batch([
        # tb_items
        
        
        libsql_client.Statement(
            """CREATE TABLE tb_items (
                    item_id varchar(32) PRIMARY KEY,
                    item_name VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255),
                    FOREIGN KEY(user_id) REFERENCES tb_users(user_id)
                    )"""
        ),
        
        libsql_client.Statement("""INSERT INTO tb_items (item_id, item_name, user_id) VALUES (?, ?, ?)""", 
            ["0d624b111f53408ab6242ed5ad9cadb9", "maggi", "1e92ff25cd3245f3920672295ae8c8b7"]),
        
        libsql_client.Statement("""INSERT INTO tb_items (item_id, item_name, user_id) VALUES (?, ?, ?)""", 
            ["0ca8e83fa38944c39301df70d7163de3", "sauce", "1e92ff25cd3245f3920672295ae8c8b7"])
    
    ])

    rs = client.execute("SELECT * FROM tb_items")

    if len(rs) > 0:
        print("The following data has been added: \n")
        for row in rs:
            print(row)
            
    #######################################
    
    client.batch([
        # tb_inventory_items

        
        libsql_client.Statement(
            """CREATE TABLE tb_inventory_items (
                    item_id varchar(32) NOT NULL,
                    inventory_id varchar(32) NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES tb_users(user_id),
                    FOREIGN KEY(item_id) REFERENCES tb_items(item_id),
                    FOREIGN KEY(inventory_id) REFERENCES tb_inventory(inventory_id)
                    )"""
        ),
        
        libsql_client.Statement("""INSERT INTO tb_inventory_items (item_id, inventory_id, user_id) VALUES (?, ?, ?)""", 
            ["0d624b111f53408ab6242ed5ad9cadb9", "a9504954a98c4b71bfe6e032b8e40ab1", "1e92ff25cd3245f3920672295ae8c8b7"]),
        
        libsql_client.Statement("""INSERT INTO tb_inventory_items (item_id, inventory_id, user_id) VALUES (?, ?, ?)""", 
            ["0ca8e83fa38944c39301df70d7163de3", "a9504954a98c4b71bfe6e032b8e40ab1", "1e92ff25cd3245f3920672295ae8c8b7"]),
    ])

    rs = client.execute("SELECT * FROM tb_inventory_items")

    if len(rs) > 0:
        print("The following data has been added: \n")
        for row in rs:
            print(row)
    

except Exception as e:
    print("There was an error...")
    print(e)
       
client.close()
    


