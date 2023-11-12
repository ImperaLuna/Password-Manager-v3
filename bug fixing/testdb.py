import sqlite3

# Create and connect to the database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        name TEXT,
        value TEXT
    )
''')

# Insert a sample record into the database
cursor.execute("INSERT INTO data (name, value) VALUES (?, ?)", ("TestName", "TestValue"))
conn.commit()

# Retrieve the record from the database
cursor.execute("SELECT * FROM data")
result = cursor.fetchone()
if result:
    name_from_db, value_from_db = result
else:
    name_from_db, value_from_db = "No Name", "No Value"

# Print the retrieved record
print(f"Name from the database: {name_from_db}")
print(f"Value from the database: {value_from_db}")

# Close the database connection
conn.close()
