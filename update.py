import psycopg2
from config import config

def update_number_vendor(vendor_phone_number, vendor_name):
    """ update vendor name based on the vendor_name """
    sql = """ UPDATE phonebook
                SET vendor_name = %s
                WHERE vendor_phone_number = %s"""
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(sql, (vendor_name, vendor_phone_number))

        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


# update name by phone number
update_number_vendor("1", "AAAAAAAAAAA")