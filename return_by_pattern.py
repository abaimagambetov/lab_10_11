from config import config
import psycopg2

conn = None

try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    filter_word = input("Hello! Please write the type of pattern you want to search (by part of name, surname, phone number): ")

    if filter_word == 'name':
        entering_name = input('Enter the name/part of the name: ')
        phonebook = "SELECT * FROM phonebook WHERE vendor_name LIKE '%{}%'".format(entering_name)
        cur.execute(phonebook)
        data = cur.fetchall()

        for user in data:
            print(*user)

    if filter_word == 'surname':
        entering_name = input('Enter the name/part of the name: ')
        phonebook = "SELECT * FROM phonebook WHERE vendor_name LIKE '%{}%'".format(entering_name)
        cur.execute(phonebook)
        data = cur.fetchall()

        for user in data:
            print(*user)

    elif filter_word == 'phone number':
        entering_phone = input('Enter the phone number: ')
        phonebook = "SELECT * FROM phonebook WHERE vendor_phone_number LIKE '%{}%'".format(entering_phone)
        cur.execute(phonebook)
        data = cur.fetchall()

        for user in data:
            print(*user)

    conn.commit()


except(Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()

