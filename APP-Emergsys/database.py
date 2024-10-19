import mysql.connector
from mysql.connector import Error
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


cursor = database.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS instalador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mail VARCHAR(100) UNIQUE,
    password VARCHAR(100) NOT NULL,
    activo BOOLEAN,
    fecha_alta DATE NOT NULL
);
"""

# Execute the query
cursor.execute(create_table_query)

# Commit changes and close the connection
database.commit()


create_table_query = """
CREATE TABLE IF NOT EXISTS barrios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE,
    mailadmin VARCHAR(100) NOT NULL,
    mailinst VARCHAR(100) NOT NULL,
    fecha_alta DATE NOT NULL
);
"""

# Execute the query
cursor.execute(create_table_query)

# Commit changes and close the connection
database.commit()




create_table_query = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mail VARCHAR(100) UNIQUE,
    password VARCHAR(100) NOT NULL,
    fecha_alta DATE NOT NULL,
    barrio1 VARCHAR(100),
    barrio2 VARCHAR(100),
    barrio3 VARCHAR(100)
    
);
"""

# Execute the query
cursor.execute(create_table_query)

# Commit changes and close the connection
database.commit()





create_table_query = """
CREATE TABLE IF NOT EXISTS placas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mac VARCHAR(100) UNIQUE,
    barrio VARCHAR(100),
    instalador VARCHAR(100),
    fecha_alta DATE NOT NULL
);
"""

# Execute the query
cursor.execute(create_table_query)

# Commit changes and close the connection
database.commit()



create_table_query = """
CREATE TABLE IF NOT EXISTS alertas_barrios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL,
    barrio VARCHAR(100) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    fecha DATETIME NOT NULL
);
"""

# Execute the query
cursor.execute(create_table_query)

# Commit changes and close the connection
database.commit()



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
