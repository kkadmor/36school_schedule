import sqlite3
con = sqlite3.connect('database.db')
cur = con.cursor()
 
cur.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
            name TEXT,
            email TEXT
            )
''')
con.commit()

def close_db():
    con.close()

def get_email_by_name(name:str):
    cur.execute('SELECT email FROM Teachers WHERE name = ?', (name,))

    email_tuple = cur.fetchone()
    if email_tuple != None:
        return email_tuple[0]
    else:
        return None


if __name__ == '__main__':
    con.close()