import sqlite3

def get_cursor():
    '''
    Returns stemapp.db cursor and db connector
    '''

    conn = get_connection()
    c = conn.cursor()
    return c, conn

def get_connection():
    conn = sqlite3.connect('stemapp.db')
    return conn

def delete_db():
    curs = get_cursor()
    curs.execute("DROP TABLE IF EXISTS casts")
    curs.execute("DROP TABLE IF EXISTS voted")
    curs.execute("DROP TABLE IF EXISTS hashes")
    curs.close()

def create_db():
    curs, __ = get_connection
    curs.execute("CREATE TABLE casts(mdwID TEXT, timestamp TEXT)")
    curs.execute("CREATE TABLE voted(studNr BLOB)")
    curs.execute("CREATE TABLE hashes(hash TEXT)")
    curs.close()