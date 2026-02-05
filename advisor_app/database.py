import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="Samsung_Phones",
        user="postgres",
        password="roza",
        host="localhost",
        port="5432"
    )
