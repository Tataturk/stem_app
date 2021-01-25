import sqlite3

def connectiondb():
    conn = sqlite3.connect('stemapp.db')

    c = conn.cursor()

    return c


#c.execute('''CREATE TABLE casts(mdwID INTEGER, timestamp TEXT)''')
#conn.commit()