import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword",     # replace with your actual password
    database="WordleProject"   # make sure this DB exists
)

# Create a cursor
cursor = conn.cursor()

print(cursor)

# # Example: insert data
# cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", ("Alice", 21))
# conn.commit()

# # Example: read data
cursor.execute("SELECT * FROM definitions")

rows = cursor.fetchall()
for row in rows:
    print(row)

# Cleanup
cursor.close()
conn.close()
