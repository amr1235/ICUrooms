import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def connect () :
    DB = mysql.connector.connect(user=os.getenv('user'), password=os.getenv('password'),
                              host=os.getenv('host'), database="icu")
    return DB
    