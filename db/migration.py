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
        # tb_users
        libsql_client.Statement("DROP TABLE IF EXISTS tb_users"),
        
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
            [uuid.uuid4().hex, "akhil", "sharma", "akhilsharma.cse@gmail.com", "1212j1h2g3jhgxj1bh23gjxg1b3gj1bgdbj23h1g"]),
        
        libsql_client.Statement("""INSERT INTO tb_users (user_id, first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?, ?)""", 
            [uuid.uuid4().hex, "atul", "ramkrishnan", "atulramkrishnan@gmail.com", "oqiunc8q278nyrc2]3-rer9uvnhercwnoeuiqry"]),
            
        libsql_client.Statement("""INSERT INTO tb_users (user_id, first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?, ?)""", 
            [uuid.uuid4().hex, "samurai", "jack", "samuraijack@cn.ca", "kjdgbcauxyg298379dp39012p9xn  2137xb  039n8c3749  87nx"]),
        
        libsql_client.Statement("""INSERT INTO tb_users (user_id, first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?, ?)""", 
            [uuid.uuid4().hex, "potato", "fucker", "potatomonstaer@gmail.com", "12323xd243.x234.x234= .4x=    .234=x. 234x    2343"])
    ])

    rs = client.execute("SELECT * FROM tb_users")

    if len(rs) > 0:
        print("The following data has been added: \n")
        for row in rs:
            print(row)

except Exception as e:
    print("There was an error...")
    print(e)
       
client.close()
    


