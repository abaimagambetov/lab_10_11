import psycopg2
from config import config


def insert_vendor(vendor_name, vendor_phone_number):
    """ insert a new vendor into the vendors table """
    global final

    sql = """INSERT INTO phonebook(vendor_name, vendor_phone_number)
             VALUES(%s, %s) RETURNING *;"""
    conn = None

    try:
        # connect to the postgresSQL database
        params = config()
        conn = psycopg2.connect(**params)
        # create a new cursor object
        cur = conn.cursor()

        record = (vendor_name, vendor_phone_number)
        # execute the INSERT statement with the input values
        cur.execute(sql, record)
        # get the generated id back
        final = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return final


# insert multiple rows
# def insert_vendor_list(vendor_list):
#     arr = []
#
#     for i in range(len(vendor_list) - 1):
#         flag = True
#         adder1 = ""
#         adder2 = ""
#
#         for j in range(len(vendor_list[i]) - 1):
#             if vendor_list[i][j] != ',' and flag:
#                 adder1 += vendor_list[i][j]
#                 flag = False
#             if vendor_list[i][j] != ',' and not flag:
#                 adder2 += vendor_list[i][j]
#
#         arr.append(tuple(adder1 + " " + adder2))
#
#     """ insert multiple vendors into the vendors table  """
#     sql = """INSERT INTO phonebook(vendor_name, vendor_phone_number)
#                  VALUES(%s, %s) RETURNING *;"""
#     conn = None
#     try:
#         # read database configuration
#         params = config()
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(**params)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.executemany(sql,arr)
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#
#     finally:
#         if conn is not None:
#             conn.close()


# insertion from a console (input)
name = "Amir"
number = "123123123"
insert_vendor(name, number)
# insert_vendor_list(["Dana,123", "Alan,321", "Mike,789"])