from flask import Blueprint, redirect, render_template, session, request,flash
from routes.check import check
import mysql.connector
from config.DB import connect

tech = Blueprint('tech', __name__)

# database config
DB = connect()
cursor = DB.cursor(buffered=True)
cursor_ = DB.cursor(buffered=True)


@tech.route('/technicians')
def tech_home():
    if check() == 'technicians':
        # get data from db and show them
        # get from fix the devices related to tech (getDevices)
        # get detailed info about the devices      (getDeviceInfo)
        DB.commit()
        tech_id = session['username']
        all_devices_data = getDeviceInfo(getDevices())
        techInfo = get_techincian_info(tech_id)
        return render_template('technician.html', lista=all_devices_data,techInfo = techInfo)
    else:
        return redirect('/')


def getDevices():
    id = session['username']
    sql = f"SELECT device_id FROM fix WHERE technician_id = {id}"
    cursor.execute(sql)
    device_DSNs = cursor.fetchall()  # [(),(),()]
    return device_DSNs


def getDeviceInfo(d_DSNs):
    all_devices_data = []
    for d_DSN in d_DSNs:
        sql = f"SELECT name,room_N,DSN FROM devices WHERE DSN={d_DSN[0]}"
        cursor_.execute(sql)
        item = cursor_.fetchone()
        all_devices_data.append(item)
    return all_devices_data  # list of [Device name,room num]

# get techincian info


def get_techincian_info(tech_id):
    get_info = "SELECT * FROM technicians WHERE id = %s" %(tech_id)
    cursor.execute(get_info)
    info = cursor.fetchone()
    return {
        'firstName': info[0],
        'lastName': info[1],
        'phone': info[4],
        'email': info[5]
    }

# update tech info
@tech.route("/technicians/updateInfo", methods=["GET", "POST"])
def update_tech_info():
    if request.method == "GET":
        return redirect('/technicians')
    if check() != "technicians":
        return redirect('/')
    tech_id = session['username']
    (firstName, lastName, phone, email) = (
        request.form['firstName'], request.form['lastName'], request.form['phone'], request.form['email'])
    update_info = "UPDATE technicians SET fname = '%s', lname = '%s', phone = '%s', email = '%s' WHERE id = %s"%(firstName,lastName,phone,email,tech_id)
    cursor.execute(update_info)
    DB.commit()
    flash("your information has been updated",'info')
    return redirect('/technicians')

#update tech password 
@tech.route('/technicians/updatePassword',methods=['GET','POST'])
def update_tech_password():
    if request.method == "GET" : return redirect('/technicians')
    if check() != "technicians" : return redirect('/')
    tech_id = session['username']
    oldPassword = request.form['oldPassword']
    get_real_password = "SELECT password FROM technicians WHERE id = %s"%(tech_id)
    cursor.execute(get_real_password)
    realPassword = cursor.fetchone()[0]
    if realPassword == oldPassword : 
        update_password = "UPDATE technicians SET password = %s WHERE id = %s" % (request.form['newPassword'], tech_id)
        cursor.execute(update_password)
        DB.commit()
        flash("your password has been updated",'password')
        return redirect('/technicians')
    else : 
        flash("your old password is incorrect",'password')
        return redirect('/technicians')

#whene the technician finished fixing the device
@tech.route('/technicians/finished')
def device_finished():
    if check() != 'technicians' : return redirect('/')
    if request.args.get('Dsn') == None : return redirect('/technicians')
    Dsn = request.args.get('Dsn')
    tech_id = session['username']
    # change the device status 
    update_device_status = "UPDATE devices SET status = 1 WHERE DSN=%s"%(Dsn,)
    cursor.execute(update_device_status)
    DB.commit()
    #change technician status
    get_numbers_of_dev = "SELECT busyOrNot FROM technicians WHERE id = %s"%(tech_id,)
    cursor.execute(get_numbers_of_dev)
    busyOrNot = cursor.fetchone()[0]
    busyOrNot = busyOrNot - 1
    set_get_numbers_of_dev = "UPDATE technicians SET busyOrNot = %s WEHERE id = %s"%(busyOrNot,tech_id)
    cursor.execute(set_get_numbers_of_dev)
    DB.commit()
    # delete the realation between the tech and the device 
    delete = "DELETE FROM fix WHERE device_id=%s AND technician_id=%s"%(Dsn,tech_id)
    cursor.execute(delete)
    DB.commit()
    flash("thank you for fixing the device")
    return redirect('/technicians')
    
