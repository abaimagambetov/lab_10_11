import psycopg2
from config import config

def delete():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        name_phone = input('Name or phone to delete the user: ')

        if name_phone.isnumeric():
            phonebook = "DELETE FROM phonebook WHERE vendor_phone_number = '{}'".format(name_phone)
        else:
            phonebook = "DELETE FROM phonebook WHERE vendor_name = '{}'".format(name_phone)

        cur.execute(phonebook)
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


delete()