import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_aiven():
    """Connect to Aiven MySQL using environment variables"""
    
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl_disabled=False
        )
        
        print("Conectado ao MySql da Aiven")
        return conn
        
    except Error as e:
        print(f"Erro de conexão: {e}")
        return None

# apenas para testar a conexão

# connection = connect_to_aiven()

# if connection:
#     cursor = connection.cursor()
#     cursor.execute("SHOW TABLES")
#     for table in cursor:
#         print(f"Table: {table[0]}")
    
#     cursor.close()
#     connection.close()