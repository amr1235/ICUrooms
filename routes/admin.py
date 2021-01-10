from flask import Blueprint, redirect, render_template, session, request, url_for
from routes.check import check, userType
import mysql.connector

ad = Blueprint('admin' ,__name__)

# database config
DB = mysql.connector.connect(
    host="localhost", user="farook", passwd="sql123", database="icu")
cursor = DB.cursor(buffered=True)
cursor_ = DB.cursor(buffered=True)


@ad.route('/admin')
def admin_home():
    if check() == 'admin' :
        return render_template('admin.html')
    return 'not admin'

# BUUUUG! check the validation of old password
@ad.route('/admin/add-user',methods=['POST','GET'])
def updateUserInfo(): 
    # check for session & validation
    if check() == 'admin' :
        if request.method == 'POST':
            # save form content
            userid = request.form['id']
            oldPassword = request.form['oldpassword']
            userpassword = request.form['newpassword']
            user_type = userType(userid)
            # update info on database
            sql = "UPDATE %s SET password=%s WHERE id=%s"%(user_type,userpassword,userid)
            cursor.execute(sql)
            DB.commit()
            return 'DATA UPDATED'
        else:
            return 'ERORR 404'
        return 'Admin Page'
    return 'ERORR 404 admin not found'

@ad.route('/admin/to-tech',methods=['POST','GET'])
def reportTech():
    if request.method == 'POST':
        # collect form data    
        all_data = request.form['device']
        # device = request.form['device']
        # room_no = request.form['room_no']
        # free_tech_id = request.form['free_tech_id']
        
        # send the data to technician
        return redirect(url_for('tech.tech_home', data=all_data))

@ad.route('/admin/free-technicains')
def getFreeTech():
    # select free technician
    sql = "SELECT id FROM technicians WHERE busyOrNot=0"
    cursor.execute(sql)
    free_tech_id = cursor.fetchone()[0]
    # tech become busy
    sql2 = f"UPDATE technicians SET busyOrNot=1 WHERE id={free_tech_id}"
    cursor_.execute(sql2)
    DB.commit()
    return render_template('admin.html',free_tech_id=free_tech_id)
    