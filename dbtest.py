import sqlite3 

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#print(cursor.execute('SELECT * FROM Topic ').fetchall())
print("Text Table count: ", cursor.execute('SELECT COUNT(*) FROM Image').fetchall())
print(cursor.execute("Image Table count: ", 'SELECT COUNT(*) FROM Image').fetchall())
