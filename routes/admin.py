from flask import Blueprint, redirect, render_template, session, request, url_for
from routes.check import check, userType
import mysql.connector
from config.DB import connect

ad = Blueprint('admin' ,__name__)

# database config
DB = connect()
cursor = DB.cursor(buffered=True)
cursor_ = DB.cursor(buffered=True)


@ad.route('/admins')
def admin_home():
    if check() == 'admins' :
        return render_template('admin.html')
    return 'not admin'

# BUUUUG! check the validation of old password
@ad.route('/admins/add-user',methods=['POST','GET'])
def updateUserInfo(): 
    # check for session & validation
    if check() == 'admins' :
        if request.method == 'POST':
            # save form content
            userid = request.form['id']
            #oldPassword = request.form['oldpassword']
            userpassword = request.form['newpassword']
            user_type = userType(userid)
            # update info on database
            sql = "UPDATE %s SET password=%s WHERE id=%s"%(user_type,userpassword,userid)
            cursor.execute(sql)
            DB.commit()
            return 'DATA UPDATED'
        else:
            return 'ERORR 404'
    return 'ERORR 404 admin not found'

@ad.route('/admins/to-tech',methods=['POST','GET'])
def reportTech():
    if request.method == 'POST':
        # collect form data   
        free_tech_id = request.form['free_tech_id']
        device_DSN = request.form['device_DSN']
        #room_no = request.form['room_no'] 
        # update data on database
        sql = f"INSERT INTO fix (technician_id,device_id)VALUES({free_tech_id},{device_DSN})"
        cursor.execute(sql)
        DB.commit()
        message = "DATA UPDATED SUCCESSFULLY"
        # send the data to technician
        return render_template('admin.html', message=message)
    else:
        return 'error 404'

@ad.route('/admins/free-technicains', methods=['POST','GET'])
def getFreeTech():
    if request.method == 'POST':
        # select free technician
        sql = "SELECT id FROM technicians WHERE busyOrNot=0"
        cursor.execute(sql)
        free_tech_id = cursor.fetchone()[0]
        # tech become busy
        sql2 = f"UPDATE technicians SET busyOrNot=1 WHERE id={free_tech_id}"
        cursor_.execute(sql2)
        DB.commit()
        return render_template('admin.html',free_tech_id=free_tech_id)
    else:
        return 'ERROR 404'
        
# if any updates occur
@ad.route('/admins/inform-patient', methods=['POST','GET'])
def inform_patient():
    if request.method == 'POST':
        patient_id =request.form['p_id']
        msg = request.form['msg']
        # send it to the patient
        sql = "UPDATE `patients` SET `msg` = '%s' WHERE `patients`.`id` = %s;"%(msg,
         patient_id)
        cursor.execute(sql)
        DB.commit()
        message = 'Message Was Sent'
        return render_template('admin.html' , message=message)
    else:
        return 'oooooooooooooooops'

# @ad.route('/admin/inform-doctor', methods=['POST','GET'])
# def inform_doctor():
#     if request.method == 'POST':
#         # collect form data (doctorID)
#         doc_id = request.form['id']
#         # get info required from database (pat)
#         # send it to the doctor

#  الادمن بيعدل فى الداتا بيز وكله ياخد من الداتا بيز