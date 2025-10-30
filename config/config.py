import os
from dotenv import load_dotenv
import mysql.connector

# Завантаження змінних із .env
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

def connect_to_db():
    db_config = load_db_config()
    connection = mysql.connector.connect(**db_config)
    return connection
