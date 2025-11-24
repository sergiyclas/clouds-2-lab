import os
import time
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def load_db_config():
    """Зчитує конфігурацію бази з .env"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'database': os.getenv('DB_NAME', 'online-banking-db'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

def wait_for_db(db_config, retries=60, delay=2):
    print(f"🔎 Trying to connect to {os.getenv('DB_HOST', 'None')}:{int(os.getenv('DB_PORT', 'None'))} as {os.getenv('DB_USER', 'None')} and database {os.getenv('DB_NAME', 'None')}")
    for i in range(retries):
        try:
            conn = mysql.connector.connect(**db_config)
            print("Connected to DB")
            return conn
        except mysql.connector.Error as e:
            print(f"DB error: {e} | retry {i+1}/{retries}")
            time.sleep(delay)
    raise Exception("Cannot connect to DB after several retries")


def connect_to_db():
    db_config = load_db_config()
    db_connection = mysql.connector.connect(**db_config)
    # connection = mysql.connector.connect(**db_config)

    return db_connection
