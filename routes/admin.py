from flask import Blueprint, redirect, render_template, session, request, url_for, flash
from routes.check import check, userType
import mysql.connector
from config.DB import connect
from random import randint
import io
import random
import string
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ad = Blueprint('admin', __name__)

# database config
DB = connect()
cursor = DB.cursor(buffered=True)
cursor_ = DB.cursor(buffered=True)


@ad.route('/admins')
def admin_home():
    if check() == 'admins':
        DB.commit()
        freeTechs = getFreeTech()
        techs = getTechs()
        patientsInfo = get_patients_info()
        rooms = getRooms()
        devices = getDevices()
        return render_template('admins.html', freeTechs=freeTechs, techs=techs, patientsInfo=patientsInfo,rooms=rooms,devices=devices)
    return redirect('/')

@ad.route('/admins/to-tech', methods=['POST', 'GET'])
def reportTech():
    if check() != "admins":
        return redirect('/')
    if request.method == 'POST':
        # collect form data
        tech_id = request.form['tech_id']
        id = int(tech_id.split('|')[0])
        device_DSN = request.form['device_DSN']
        # update data on database
        sql = f"INSERT INTO fix (technician_id,device_id)VALUES({id},{device_DSN})"
        cursor.execute(sql)
        DB.commit()
        # change the device status
        update_device_status = "UPDATE devices SET status = 0 WHERE DSN=%s" % (
            device_DSN,)
        cursor.execute(update_device_status)
        DB.commit()
        # change technician busy or not
        get_numbers_of_dev = "SELECT busyOrNot FROM technicians WHERE id = %s"%(tech_id,)
        cursor.execute(get_numbers_of_dev)
        busyOrNot = cursor.fetchone()[0]
        busyOrNot = busyOrNot + 1
        set_get_numbers_of_dev = "UPDATE technicians SET busyOrNot = %s WEHERE id = %s"%(busyOrNot,tech_id)
        cursor.execute(set_get_numbers_of_dev)
        DB.commit()
        flash('DATA UPDATED SUCCESSFULLY', 'reportTech')
        return redirect('/admins#report')
    else:
        return redirect('/admins')
# get free tchs


def getFreeTech():
    # select free technician
    sql = "SELECT fname,lname,id FROM technicians WHERE busyOrNot=0"
    cursor.execute(sql)
    free_tech_ids = cursor.fetchall()
    return free_tech_ids

# get all tech ids


def getTechs():
    sql = "SELECT fname,lname,id,busyOrNot FROM technicians"
    cursor.execute(sql)
    techs = cursor.fetchall()
    return techs
# if any updates occur


@ad.route('/admins/inform-patient', methods=['POST', 'GET'])
def inform_patient():
    if check() != "admins":
        return redirect('/')
    if request.method == 'POST':
        patient_id = int(request.form['patient_id'].split('|')[0])
        scan_image = request.files['patient-scan']
        if scan_image.filename == '':
            return redirect('/admins')
        # send it to the patient
        binaryData = scan_image.stream.read()
        # print(dir(binaryData))
        sql = """INSERT INTO scans (patient_id,patient_scan) VALUES (%s,%s)"""
        try:
            tuble = (patient_id, binaryData)
            cursor.execute(sql, tuble)
            DB.commit()
            flash("the scan has been sent to the patient", "inform-patient")
            return redirect('/admins')
        except:
            flash("there is somthing wrong please try again", "inform-patient")
            return redirect('/admins')
    else:
        return redirect('/admins#message')

# get patients info


def get_patients_info():
    sql = "SELECT fname,lname,id FROM patients"
    cursor.execute(sql)
    return cursor.fetchall()

# generating id for specific table


def generate_id(table_name):
    # get all the ids from the table
    sql = "SELECT id from %s " % (table_name,)
    cursor.execute(sql)
    idsT = cursor.fetchall()
    idsList = [id[0] for id in idsT]
    isInList = True
    Id = ""
    while(isInList):
        Id = str(randint(1, 9))

        for i in range(0, 6):
            Id += str(randint(1, 9))

        lastTwoDigits = ""

        if table_name == "doctors":
            lastTwoDigits = "00"
        elif table_name == "patients":
            lastTwoDigits = "01"
        elif table_name == "technicians":
            lastTwoDigits = "11"
        else:
            lastTwoDigits = "10"
        Id += lastTwoDigits
        if(int(Id) not in idsList):
            isInList = False
    # now i have id not in the table
    return int(Id)


@ad.route('/admins/insertUser', methods=['GET', 'POST'])
def insertUser():
    if check() != "admins":
        return redirect('/')
    if request.method != "POST":
        return redirect('/admins')
    (firstName, lastName, email, phone, table_name) = (
        request.form['firstName'], request.form['lastName'], request.form['email'], request.form['phone'], request.form['table_name'])
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for i in range(8))
    id = generate_id(table_name)
    # admins does't have phone numbers so
    insert_Data = ""
    values = tuple()
    if table_name == "admins":
        insert_Data = "INSERT INTO admins (fname,lname,id,email,password) VALUES (%s,%s,%s,%s,%s)"
        values = (firstName, lastName, id, email, password)
    elif table_name == "doctors":
        insert_Data = "INSERT INTO doctors (fname,lname,id,Email,password,phone) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (firstName, lastName, id, email, password, int(phone))
    elif table_name == "patients":
        roomNum = request.form['roomNum']
        insert_Data = "INSERT INTO patients (fname,lname,id,Email,password,phone,room_N) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values = (firstName, lastName, id, email, password, int(phone),roomNum)
        #update number of empty beds 
        sql = "SELECT empty_beds_number FROM rooms WHERE room_number = %s"%(roomNum)
        cursor.execute(sql)
        number = cursor.fetchone()[0]
        number = number - 1
        sql2 = "UPDATE rooms SET empty_beds_number = %s WHERE room_number= %s"%(number,roomNum)
        cursor.execute(sql2)
        DB.commit()
    elif table_name == "technicians":
        insert_Data = "INSERT INTO technicians (fname,lname,id,Email,password,phone,busyOrNot) VALUES (%s,%s,%s,%s,%s,%s,0)"
        values = (firstName, lastName, id, email, password, int(phone))
    cursor.execute(insert_Data, values)
    DB.commit()
    # send user data to his email
    send_email(email,"""your id : %s your password : %s"""%(id,password))
    flash('DATA UPDATED SUCCESSFULLY', 'addUser')
    return redirect('/admins#register')

# send email


def send_email(email,mess):
    smtp_server = "smtp.gmail.com"
    port = 465  # For starttls
    sender_email = "amrali.635241@gmail.com"
    receiver_email = email  # Enter receiver address
    password = "amrali2031999"
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
     
    text = mess
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        
# add new room 
@ad.route('/admins/addNewRoom',methods=['GET','POST'])
def addNewRoom() :
    if check() != 'admins' : return redirect('/')
    if request.method == "GET" : return redirect('/admins')
    roomNum = request.form['roomNum']
    bedsNum = request.form['bedsNum']
    add_new_room = "INSERT INTO rooms (room_number,empty_beds_number) VALUES (%s,%s)"%(roomNum,bedsNum)
    cursor.execute(add_new_room)
    DB.commit()
    flash("A new room has been added","room")
    return redirect('/admins#room')

#get rooms info 
def getRooms():
    sql = "SELECT * FROM rooms"
    cursor.execute(sql)
    rooms = cursor.fetchall()
    return rooms
# add new device 
@ad.route('/admins/addNewDevice',methods=['GET','POST'])
def addNewDevice():
    if check() != "admins" : return redirect('/')
    if request.method == "GET" : return redirect('/admins')
    (deviceName,Dsn,roomNum) = (request.form['deviceName'],request.form['Dsn'],request.form['roomNum'])
    
    insert_new_device = """INSERT INTO devices (room_N,DSN,name) VALUES (%s,%s,%s)"""
    values = (roomNum,Dsn,deviceName)
    print(insert_new_device)
    cursor.execute(insert_new_device,values)
    DB.commit()
    flash("A new device has been added",'devices')
    return redirect('/admins#device')

#get devices 
def getDevices():
    sql = "SELECT * FROM devices "
    cursor.execute(sql)
    devices = cursor.fetchall()
    return devices
    
