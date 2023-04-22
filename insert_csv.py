import psycopg2
import csv
from config import config

arr = []
with open('phone_numbers.csv') as f:
    read = csv.reader(f, delimiter=',')

    for row in read:
        arr.append(tuple(row))

sql = """
    INSERT INTO phonebook(vendor_name, vendor_phone_number)
    VALUES(%s, %s);
    """
conn = None
try:
    params = config()
    conn = psycopg2.connect(**params)

    cur = conn.cursor()
    cur.executemany(sql, arr)

    conn.commit()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()