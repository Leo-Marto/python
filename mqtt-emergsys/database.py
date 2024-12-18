import mysql.connector
import os
import time
from dotenv import load_dotenv

load_dotenv()


hostenv = os.getenv('HOST_DB')
userenv = os.getenv('USER_DB')
passwordenv = os.getenv('PASS_DB')
databaseenv = os.getenv('DATABASE_DB')


database = mysql.connector.connect(
    host=hostenv,  # Cambiar según tu configuración
    user=userenv,       # Cambiar según tu usuario de MySQL
    password=passwordenv,       # Cambiar según tu password de MySQL
    database=databaseenv  # Base de datos que creaste
)





# def connect_to_mysql():
#     try:
#         # Attempt to connect to the database
#         db = mysql.connector.connect(
#             host=hostenv,  # Cambiar según tu configuración
#             user=userenv,       # Cambiar según tu usuario de MySQL
#             password=passwordenv,       # Cambiar según tu password de MySQL
#             database=databaseenv  # Base de datos que creaste
#         )
#         print("Connection successful!")
#         return db
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None

# # Retry connecting up to 5 times with a delay of 5 seconds
# retries = 5
# for attempt in range(retries):
#     connection = connect_to_mysql()
#     if connection:
#         break
#     print(f"Retrying in 5 seconds... ({attempt + 1}/{retries})")
#     time.sleep(5)

# if connection is None:
#     print("Failed to connect to the MySQL database after multiple attempts.")
