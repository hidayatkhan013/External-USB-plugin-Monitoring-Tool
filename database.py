import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_project(conn, project):
    sql = ''' INSERT INTO PC_details(pc_name,pc_user,pc_ip,pc_mac,pc_workgroup)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def select_all_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM PC_details")
    rows = cur.fetchall()

def createTabale(database,conn):
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS PC_details (
                                        pc_name text,
                                        pc_user text,
                                        pc_ip text,
                                        pc_mac text,
                                        pc_workgroup text
                                    ); """
    conn = create_connection(database)
    if conn is not None:
        c = conn.cursor()
        c.execute(sql_create_projects_table)
    else:
        print("Error! cannot create the database connection.")

def main_db(data):
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    with conn:
        # create a new project
        createTabale(database,conn)
        project = data
        project_id = create_project(conn, project)
        select_all_tasks(conn)

