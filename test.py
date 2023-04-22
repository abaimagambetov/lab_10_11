from config import config
import psycopg2

conn = None
cur = None


def insert_update():
    try:
        phonebook_insert = ''' INSERT INTO phonebook (vendor_name, vendor_phone_number)
                    VALUES (%s, %s)'''
        phonebook_update = ''' UPDATE phonebook SET vendor_phone_number = %s WHERE vendor_name = %s '''
        existing = ''' SELECT vendor_name FROM phonebook WHERE vendor_name = %s '''
        name, phone = input().split()
        users = []
        while phone != 'stop' or name != 'stop':
            users.append((name, phone))
            name, phone = input().split()
        for n, p in users:
            cur.execute(existing, [n])
            result = cur.fetchone()
            if result:
                cur.execute(phonebook_update, (p, n))
            else:
                cur.execute(phonebook_insert, (n, p))
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def filter_by():
    try:
        filter_due_to = input(
            'How do you want to filter phonebook?(by part of name, name, numbers in phone, '
            'by 2-4 numbers of phone) ')
        if filter_due_to == 'part of name' or filter_due_to == 'name':
            entering_name = input('Enter the name/part of the name: ')
            phonebook = ''' SELECT * FROM phonebook WHERE vendor_name LIKE '%{}%' '''.format(entering_name)
            cur.execute(phonebook, [entering_name])
            data = cur.fetchall()
            for user in data:
                print(*user)
        elif filter_due_to == '2-4 nums' or filter_due_to == '2-4 numbers of phone':
            entering_phone = input('2-4 numbers of vendor_phone_number: ')
            phonebook = ''' SELECT * FROM phonebook WHERE SUBSTRING(vendor_phone_number FROM 2 FOR 3) = %s '''
            cur.execute(phonebook)
            data = cur.fetchall()
            for user in data:
                print(*user)
        elif filter_due_to == 'numbers in phone' or filter_due_to == 'nums':
            entering_phone = input('numbers of phone: ')
            phonebook = ''' SELECT * FROM phonebook WHERE vendor_phone_number LIKE '%{}%' '''.format(entering_phone)
            cur.execute(phonebook)
            data = cur.fetchall()
            for user in data:
                print(*user)
        else:
            print('Please enter next time correctly')
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def pagination():
    from_user, for_user = map(int, input('From what user for what user do you want to query? ').split())
    phonebook = ''' SELECT * FROM phonebook ORDER BY vendor_name OFFSET %s LIMIT %s '''
    cur.execute(phonebook, (from_user, for_user))
    data = cur.fetchall()
    for user in data:
        print(*user)


def delete():
    try:
        name_phone = input('Name or phone to delete the user: ')
        if name_phone.isnumeric():
            phonebook = ''' DELETE FROM phonebook WHERE vendor_phone_number = %s '''
        else:
            phonebook = ''' DELETE FROM phonebook WHERE vendor_name = %s '''
        cur.execute(phonebook, [name_phone])
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    create_script = ''' CREATE TABLE IF NOT EXISTS phonebook (
        vendor_name varchar(20) NOT NULL,
        vendor_phone_number varchar(12)) '''
    cur.execute(create_script)
    want_insert_update = input('Do you want to insert new user(s)? ')
    if want_insert_update.lower() == 'yes':
        insert_update()
    want_filter = input('Do you want to filter users? ')
    if want_filter.lower() == 'yes':
        filter_by()
    want_query = input('Do you want to query data? ')
    if want_query.lower() == 'yes':
        pagination()
    want_delete = input('Do you want to delete someone? ')
    if want_delete.lower() == 'yes':
        delete()
    conn.commit()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()