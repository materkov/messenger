import mysql.connector

conn = mysql.connector.connect(user='root', password='root',
                               host='127.0.0.1', port=3306,
                               database='messenger', autocommit=True)
# cnx.close()
#conn.autocommit(True)
