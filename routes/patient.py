from flask import Blueprint, request, render_template, redirect, url_for, session, flash, make_response, send_file
import mysql.connector
from config.middlewares import is_patient_logged_in
from config.DB import connect

patient = Blueprint("patient", __name__)

# database config
DB = connect()
cursor = DB.cursor()

@patient.route('/patients')
def patients_home():
    if is_patient_logged_in() :
        patient_id = session['username']
        DB.commit()
        doctors = get_doctors(patient_id)
        scansIds = get_patient_scans(patient_id)
        patientInfo = get_patient_info(patient_id)
        return render_template("patient.html",doctors=doctors,scansIds=scansIds,patientInfo=patientInfo)
    else : 
        return redirect('/')
    
#get the doctors that supervises the patient
def get_doctors(patient_id):
    doctors_Data = list()
    get_docs = "SELECT doctor_id FROM examine WHERE patient_id = %s"%(patient_id,)
    cursor.execute(get_docs)
    idsT = cursor.fetchall()
    idsList = [id[0] for id in idsT]
    if len(idsList) == 0 :
        return doctors_Data
    for id in idsList : 
        get_doctor = "SELECT * FROM doctors WHERE id = %s"%(id,)
        cursor.execute(get_doctor)
        doctorData = cursor.fetchone()
        data = {
            'firstName' : doctorData[0],
            'lastName'  : doctorData[1],
            'id'        : doctorData[2],
            'phone'     : str("0" + str(doctorData[4])),
            'email'     : doctorData[6]
        }
        doctors_Data.append(data)
    return doctors_Data

# get the scans of the ptient 
def get_patient_scans(patient_id):
    if is_patient_logged_in():
        get_scans = "SELECT scanId FROM `scans` WHERE patient_id = %s"%(patient_id)
        cursor.execute(get_scans)
        scansT = cursor.fetchall()
        scansList = [scan[0] for scan in scansT]
        return scansList
    else : 
        return redirect('/')
    
#download patient scan 
@patient.route('/patients/scans')
def download_scan():
    if(is_patient_logged_in()):
        scanId = request.args.get('scanId')
        if scanId == None : return redirect('/patients')
        get_scan = "SELECT patient_scan FROM scans WHERE scanId = %s"%(scanId)
        cursor.execute(get_scan)
        imageBinaryData = cursor.fetchone()[0]
        response = make_response(imageBinaryData)
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.set(
        'Content-Disposition', 'attachment', filename='scan%s.jpg'%scanId)
        return response
    else :
        return redirect('/')
    
# get patient data
def get_patient_info(patient_id):
    get_info = "SELECT * from patients WHERE id = %s"%(patient_id,)
    cursor.execute(get_info)
    info = cursor.fetchone()
    return {
        'firstName' : info[0],
        'lastName'  : info[1],
        'phone'     : info[4],
        'email'     : info[8]
    }

# update patient info
@patient.route('/patients/updateInfo',methods=['GET','POST'])
def update_patient_info():
    if request.method == "GET" : return redirect('/patients')
    if is_patient_logged_in() :
        patient_id = session['username']
        (firstName,lastName,email,phone) = (request.form['firstName'],request.form['lastName'],request.form['email'],request.form['phone'])
        update_info = "UPDATE patients SET fname = '%s', lname = '%s', phone = '%s', email = '%s' WHERE id = %s"%(firstName,lastName,phone,email,patient_id)
        cursor.execute(update_info)
        DB.commit()
        flash('your info has been updated','info')
        return redirect('/patients')
    else : 
        return redirect('/') 

#update patient password
@patient.route('/patients/updatePassword',methods=['GET','POST'])
def update_patient_password():
    if request.method == "GET" : return redirect('/patients')
    if is_patient_logged_in() :
        patient_id = session['username']
        formPassword = request.form['oldPassword']
        get_real_password = "SELECT password FROM patients WHERE id = %s"%(patient_id)
        cursor.execute(get_real_password)
        realPassword = cursor.fetchone()[0]
        if (realPassword == formPassword) :
            update_password = "UPDATE patients SET password = %s WHERE id = %s" % (
                    request.form['newPassword'], patient_id)
            cursor.execute(update_password)
            DB.commit()
            flash("your password has been updated",'password')
            return redirect('/patients')
        else : 
            flash("old Password is incorrect",'password')
            return redirect('/patients')
    else : 
        return redirect('/')
    
    