import mysql.connector
def connect () :
    DB = mysql.connector.connect(host="localhost", user="root", passwd="mysql", database="icu")
    return DB
    