from mysql import connector
import pandas as pd
from urllib.parse import unquote

config = {
'user': 'admin',
'password': 'ohmypycis4930',
'host': "ohmypy.cdd0llcf03hp.us-east-1.rds.amazonaws.com",
'port': '3306',
'database': 'metadata',
'raise_on_warnings': True}

frontend_db = connector.connect(**config)

def insert_face(face_vector, name):
    name = unquote(name)
    name_id = get_name_id(str(name))
    get_face_id(str(face_vector), name_id)
    return 1


def get_name_id(name):
    name = unquote(name)
    sql_select_query = "SELECT MIN(name_id) FROM name_data WHERE full_name = '" + name + "'"
    cursor = frontend_db.cursor()
    cursor.execute(sql_select_query)
    records = cursor.fetchall()

    name_id = records[0][0]
    if name_id != None:
        return name_id
    else:
        cursor = frontend_db.cursor()
        cursor.execute("INSERT INTO name_data (full_name) VALUES ('" + name + "')")
        frontend_db.commit()
        cursor.close()
        return get_name_id(name)


def get_face_id(face_vector, name_id):
    sql_select_query = "SELECT MIN(face_id), count FROM face_data WHERE face_vector = '" + face_vector + "'"
    cursor = frontend_db.cursor()
    cursor.execute(sql_select_query)
    records = cursor.fetchall()

    face_id = records[0][0]
    if face_id != None:
        new_count = records[0][1] + 1
        sql_select_query = "UPDATE face_data SET count = " + str(new_count) + " WHERE face_id = " + str(face_id) + ""
        cursor = frontend_db.cursor()
        cursor.execute(sql_select_query)
        frontend_db.commit()
        cursor.close()
        return face_id
    else:
        cursor = frontend_db.cursor()
        cursor.execute("INSERT INTO face_data (face_vector, name_id, count) VALUES ('" + face_vector + "',"+str(name_id)+", 1)")
        frontend_db.commit()
        cursor.close()
        return get_face_id(face_vector, name_id)


def get_vector_data():
    sql_select_query = "select n.full_name, LEFT(CONVERT(f.face_vector USING utf8),200) face_vector, f.count from name_data n join face_data f on f.name_id = n.name_id;"
    cursor = frontend_db.cursor()
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    df = pd.DataFrame(records)

    return df