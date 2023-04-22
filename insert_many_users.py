import psycopg2
from config import config

def insert_vendors():
    """ update vendor name based on the vendor id """
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        name, phone = input().split()
        users = []

        phonebook_insert = "INSERT INTO phonebook (vendor_name, vendor_phone_number) VALUES (%s, %s)"

        while phone != 'stop' or name != 'stop':
            users.append((name, phone))
            name, phone = input().split()

        for n, p in users:
            # check for correctness
            if len(p) <= 4 or not p.isnumeric():
                print(n, 'has wrong phone number input:', p)
                continue
            cur.execute(phonebook_insert, (n, p))

        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


insert_vendors()