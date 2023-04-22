import psycopg2
from config import config

def pagination():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    from_user, for_user = map(int, input('From what user for what user do you want to query? ').split())
    phonebook = ''' SELECT * FROM phonebook ORDER BY vendor_name OFFSET %s LIMIT %s '''
    cur.execute(phonebook, (from_user, for_user))
    data = cur.fetchall()

    for user in data:
        print(*user)

    conn.commit()
    cur.close()


pagination()