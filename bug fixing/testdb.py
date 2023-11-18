import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        name TEXT,
        value TEXT
    )
''')

cursor.execute("INSERT INTO data (name, value) VALUES (?, ?)", ("TestName", "TestValue"))
conn.commit()

cursor.execute("SELECT * FROM data")
result = cursor.fetchone()
if result:
    name_from_db, value_from_db = result
else:
    name_from_db, value_from_db = "No Name", "No Value"

print(f"Name from the database: {name_from_db}")
print(f"Value from the database: {value_from_db}")

conn.close()
