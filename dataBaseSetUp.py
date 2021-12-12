import random
import string
import mysql.connector
from random import randint
import os
from dotenv import load_dotenv
load_dotenv()

def generateEmail():
       return ''.join(random.choice(string.ascii_letters) for _ in range(7)) +"@gmail.com"
# db = connector.connect()
db = mysql.connector.connect(user=os.getenv('user'), password=os.getenv('password'),
                              host=os.getenv('host'))
mycursor = db.cursor()
print("creating icu database ...")
mycursor.execute("CREATE DATABASE icu") # create dataBase
db.close()
print("database created.")
db = mysql.connector.connect(user=os.getenv('user'), password=os.getenv('password'),
                              host=os.getenv('host'),database="icu")
mycursor = db.cursor()
print("creating icu tables ...")
# create tables
mycursor.execute("CREATE TABLE rooms (empty_beds_number INT,room_number INT NOT NULL PRIMARY KEY)")
mycursor.execute("CREATE TABLE devices (name VARCHAR(255),DSN VARCHAR(255) NOT NULL PRIMARY KEY,room_N INT,FOREIGN KEY (room_N) REFERENCES rooms (room_number) )")
mycursor.execute("CREATE TABLE doctors (fname VARCHAR(255), lname VARCHAR(255),id INT NOT NULL PRIMARY KEY,Email VARCHAR(255),password VARCHAR(255),phone INT)")
mycursor.execute("CREATE TABLE technicians (fname VARCHAR(255), lname VARCHAR(255),id INT NOT NULL PRIMARY KEY,Email VARCHAR(255),password VARCHAR(255),phone INT,busyOrNot INT)")
mycursor.execute("CREATE TABLE admins (fname VARCHAR(255), lname VARCHAR(255),id INT NOT NULL PRIMARY KEY,email VARCHAR(255),password VARCHAR(255))")
mycursor.execute("CREATE TABLE patients (fname VARCHAR(255), lname VARCHAR(255),id INT NOT NULL PRIMARY KEY,Email VARCHAR(255),password VARCHAR(255),phone INT,room_N INT,FOREIGN KEY (room_N ) REFERENCES rooms(room_number))")
mycursor.execute("CREATE TABLE scans (patient_id INT NOT NULL, patient_scan LONGBLOB NOT NULL,FOREIGN KEY (patient_id) REFERENCES patients(id))")
mycursor.execute("CREATE TABLE fix (technician_id INT NOT NULL ,device_id VARCHAR(255) NOT NULL,FOREIGN KEY (technician_id) REFERENCES technicians(id),FOREIGN KEY (device_id) REFERENCES devices(DSN))")
mycursor.execute("CREATE TABLE examine (patient_id INT NOT NULL,doctor_id INT NOT NULL,examine_date DATE,FOREIGN KEY (patient_id) REFERENCES patients(id),FOREIGN KEY (doctor_id) REFERENCES doctors(id))")
mycursor.execute("CREATE TABLE events (name VARCHAR(255),doctor_id INT NOT NULL,patient_id INT NOT NULL,FOREIGN KEY (patient_id) REFERENCES patients(id),FOREIGN KEY (doctor_id) REFERENCES doctors(id))")
print("tables created.")
# insert new admin with an arbitrary password and email
(firstName, lastName, email) = ("admin", "admin", generateEmail())
letters = string.ascii_letters
password = ''.join(random.choice(letters) for i in range(8))
Id = str(randint(1, 9))
for i in range(0, 6):
    Id += str(randint(1, 9))
id = int(Id + "10")
insert_Data = "INSERT INTO admins (fname,lname,id,email,password) VALUES (%s,%s,%s,%s,%s)"
values = (firstName, lastName, id, email, password)
mycursor.execute(insert_Data, values)
db.commit()
print("===============================")
print("new admin has been created \n" + " email : " + email + "\n password : " + password+"\n ID : " + str(id))
print("===============================")
