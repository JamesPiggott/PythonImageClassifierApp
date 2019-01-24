import sqlite3

# Small script that will create the initial SQLite DB.

conn = sqlite3.connect('kerasapp_db.sqlite')

cursor = conn.cursor()

print("Opened database successfully")

cursor.execute('''CREATE TABLE users
         (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         name           VARCHAR(100)    NOT NULL,
	 email          VARCHAR(100)    NOT NULL,
	 username       VARCHAR(30)    NOT NULL,
         password       VARCHAR(100)    NOT NULL,
         register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
	);''')

conn.commit()
conn.close()


