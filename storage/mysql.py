import mysql.connector
import os

conn = mysql.connector.connect(host=os.getenv('MYSQL_HOST'), port=int(os.getenv('MYSQL_PORT')),
                               user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASS'),
                               database='messenger', autocommit=True)
# cnx.close()
#conn.autocommit(True)
