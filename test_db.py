import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="appweb",
        port=3307
    )
    print("¡Conexión exitosa!")
    conn.close()
except mysql.connector.Error as err:
    print("Error al conectar:", err)