import sqlite3 

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#print(cursor.execute('SELECT * FROM Topic ').fetchall())
print(cursor.execute('SELECT * FROM Image')).fetchall()
