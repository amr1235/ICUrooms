from flask import Blueprint, redirect, render_template, session, request
from routes.check import check
import mysql.connector

tech = Blueprint('tech' , __name__)

# database config
DB = mysql.connector.connect(
    host="localhost", user="farook", passwd="sql123", database="icu")
cursor = DB.cursor(buffered=True)
cursor_ = DB.cursor(buffered=True)


@tech.route('/technicians')
def tech_home():
    if check() == 'technicians':
        #get data from db and show them
        #get from fix the devices related to tech (getDevices)
        #get detailed info about the devices      (getDeviceInfo)
        all_devices_data = getDeviceInfo(getDevices())
        return render_template('technician.html' , lista = all_devices_data)
    # else:
    #     return 'not tech'
def getDevices():
    id = session['username']
    sql = f"SELECT device_id FROM fix WHERE technician_id = {id}"
    cursor.execute(sql)
    device_DSNs = cursor.fetchall() #[(),(),()]
    return device_DSNs

def getDeviceInfo(d_DSNs):
    all_devices_data = []
    for d_DSN in d_DSNs:
        sql = f"SELECT name,room_N FROM devices WHERE DSN={d_DSN[0]}"
        cursor_.execute(sql)
        item = cursor_.fetchone()
        all_devices_data.append(item)
    return all_devices_data # list of [Device name,room num]

    