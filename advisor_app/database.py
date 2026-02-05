
# database.py
import psycopg2

DB_CONFIG = {
    "dbname": "Samsung_Phones",
    "user": "postgres",
    "password": "roza",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
