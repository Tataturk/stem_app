import sqlite3

def get_cursor():
    '''
    Returns stemapp.db cursor
    '''
    conn = sqlite3.connect('stemapp.db')

    c = conn.cursor()

    return c


def reset_db():
    curs = get_cursor()
    curs.execute("DROP TABLE IF EXISTS casts")
    curs.execute("DROP TABLE IF EXISTS voted")

    curs.execute("CREATE TABLE casts(mdwID TEXT, timestamp TEXT)")
    curs.execute("CREATE TABLE voted(studNr INTEGER)")

    curs.close()