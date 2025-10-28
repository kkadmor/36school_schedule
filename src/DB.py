import sqlite3

class DB:

    con = sqlite3.connect('database.db')
    cur = con.cursor()

    def __init__(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
                    name TEXT,
                    email TEXT
                    )
        ''')
        self.con.commit()

    def get_email_by_name(self, name:str):
        self.cur.execute('SELECT email FROM Teachers WHERE name = ?', (name,))
        return self.cur.fetchone()[0]


if __name__ == '__main__':
    db = DB()
    db.con.close()