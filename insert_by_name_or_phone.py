import psycopg2
from config import config

def update_vendor(vendor_name, vendor_phone_number):
    """ update vendor name based on the vendor id """
    phonebook_insert = "INSERT INTO phonebook (vendor_name, vendor_phone_number) VALUES ('{}', {})".format(vendor_name, vendor_phone_number)
    phonebook_update = "UPDATE phonebook SET vendor_phone_number = {} WHERE vendor_name = '{}'".format(vendor_phone_number, vendor_name)
    existing = "SELECT vendor_name FROM phonebook WHERE vendor_name = '{}'".format(vendor_name)

    # print(phonebook_insert)
    # print(phonebook_update)
    # print(existing)

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(existing)
        result = cur.fetchone()

        if result:
            cur.execute(phonebook_update, (vendor_phone_number, vendor_name))
            print("True")
        else:
            cur.execute(phonebook_insert, (vendor_name, vendor_phone_number))
            print("False")

        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


update_vendor("Rizen", "1000")