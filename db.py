import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Y@sh1107",
    database="expense_tracker"
)

cursor = conn.cursor(dictionary=True)