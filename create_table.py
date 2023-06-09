import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    command = """
        CREATE TABLE phonebook (
            vendor_name VARCHAR(255) NOT NULL,
            vendor_phone_number VARCHAR(20) NOT NULL
        )
        """
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_tables()