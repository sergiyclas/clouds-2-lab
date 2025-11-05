import os
import time
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def load_db_config():
    """Зчитує конфігурацію бази з .env"""
    return {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

def wait_for_db(db_config, retries=15, delay=2):
    for i in range(retries):
        try:
            conn = mysql.connector.connect(**db_config)
            print("Connected to DB")
            return conn
        except mysql.connector.Error:
            print(f"DB not ready, retry {i+1}/{retries}")
            time.sleep(delay)
    raise Exception("Cannot connect to DB after several retries")


def connect_to_db():
    db_config = load_db_config()
    db_connection = mysql.connector.connect(**db_config)
    # connection = mysql.connector.connect(**db_config)

    return db_connection
