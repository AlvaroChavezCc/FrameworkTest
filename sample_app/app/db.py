import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "host": "localhost",
    "dbname": "labo",
    "user": "postgres",
    "password": "12345"
}

def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_client_encoding('UTF8')
    return conn
