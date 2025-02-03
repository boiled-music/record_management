import mysql.connector

# MariaDB 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="a12345678!",
    database="library_db"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")
for table in cursor:
    print(table)

conn.close()
