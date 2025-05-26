import psycopg2
from psycopg2 import OperationalError
from psycopg2 import Binary
from urllib.parse import urljoin
import requests
from __config__ import CONFIG_PATH

try:
    from configparser import ConfigParser
except ImportError:
    from configparser import SafeConfigParser as ConfigParser

# Used to read the .ini configuration file. This allows the script to load configuration parameters from a separate file.
config_file: ConfigParser = ConfigParser()
config_file.read(CONFIG_PATH)

DB_HOST = config_file["postgres"]["url"]
DB_PORT = config_file["postgres"]["port"]
DB_NAME = config_file["postgres"]["name"]
DB_USER = config_file["postgres"]["user"]
DB_PASSWORD = config_file["postgres"]["pwd"]


API_HOST = config_file["api"]["url"]
API_PORT = config_file["api"]["port"]
API_BASE = f"http://{API_HOST}:{API_PORT}/"
API_BASE = urljoin(API_BASE, config_file["api"]["base"])

###  DATABASE ###

def connect_to_postgres():
    """Crea una connessione al database PostgreSQL."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connessione a PostgreSQL stabilita con successo!")
        return connection
    except OperationalError as e:
        print(f"Errore durante la connessione a PostgreSQL: {e}")
        return None

def ensure_table_exist():
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS plants(
                id BIGSERIAL PRIMARY KEY,
                photo BYTEA,
                status VARCHAR,
                plant_id INTEGER,
                photo_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

            cursor.execute(create_table_query)
            connection.commit()
            print("INFO.1 = Table created / verified with success!")
            return True     
    except Exception as e:
        print("ERROR.1 = Creation table failed")
        print(f"DETAILS: {e}")
        return False

def post_photo(photo_bytes, status, plant_id):
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO plants (photo, status, plant_id)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (Binary(photo_bytes), status, plant_id))
            connection.commit()
            print("INFO.2 = Photo inserted successfully")
            return True
    except Exception as e:
        print("ERROR.2 = Failed to insert photo")
        print(f"DETAILS: {e}")
        return False

# get the photo with id = id
def get_photo(id):
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            query = "SELECT id, photo, status, plant_id, photo_timestamp FROM plants WHERE id = %s"
            cursor.execute(query, (id,))
            return cursor.fetchone()
    except Exception as e:
        print("ERROR.3 = Failed to get photo by ID")
        print(f"DETAILS: {e}")
        return None

# get the last photo pic with plant_id = plant_id
def get_last_photo(plant_id):
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            query = """
                SELECT photo
                FROM plants
                WHERE plant_id = %s
                ORDER BY photo_timestamp DESC
                LIMIT 1
            """
            cursor.execute(query, (plant_id,))
            return cursor.fetchone()
    except Exception as e:
        print("ERROR.4 = Failed to get last photo by plant_id")
        print(f"DETAILS: {e}")
        return None

# get all the photo with the status = status
def get_photos_with_status(status):
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            query = """
                SELECT id, photo, status, plant_id, photo_timestamp
                FROM plants
                WHERE status = %s
            """
            cursor.execute(query, (status,))
            return cursor.fetchall()
    except Exception as e:
        print("ERROR.5 = Failed to get photos by status")
        print(f"DETAILS: {e}")
        return []

# get all the photo with the plant_id = plant_id
def get_photos_with_plantid(plant_id):
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            query = """
                SELECT id, photo, status, plant_id, photo_timestamp
                FROM plants
                WHERE plant_id = %s
            """
            cursor.execute(query, (plant_id,))
            return cursor.fetchall()
    except Exception as e:
        print("ERROR.6 = Failed to get photos by plant_id")
        print(f"DETAILS: {e}")
        return []

# get all the photo with the plant_id = plant_id and status = status
def get_photos_with_plantid_and_status(plant_id, status):
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            query = """
                SELECT id, photo, status, plant_id, photo_timestamp
                FROM plants
                WHERE plant_id = %s AND status = %s
            """
            cursor.execute(query, (plant_id, status))
            return cursor.fetchall()
    except Exception as e:
        print("ERROR.7 = Failed to get photos by plant_id and status")
        print(f"DETAILS: {e}")
        return []

## API
def get_plant(plant_id):
    api_get_path = API_BASE + "/" + str(plant_id)
    response = requests.get(api_get_path)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

def get_plants():
    response = requests.get(API_BASE)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

def patch_plant(plant_id, current_status, new_status):
    #print(f"PATCH: {plant_id} in {current_status} -> {new_status}")
    
    api_patch_path = API_BASE + "/" + str(plant_id)
    response = requests.patch(api_patch_path, data={'statusNew': new_status})
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


if __name__ == "__main__":
    print("## TEST GET ##")
    print(f"ID: 1 - Status: {get_plant(1)['status']}")

    print("## TEST PATCH ##")
    print(patch_plant(1, "Healthy", "Sick"))
    
    plants = get_plants()
    for plant in plants:
        print(f"ID: {plant['plantId']} -  Status: {plant['status']}")