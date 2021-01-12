from flask import Blueprint, request, render_template, redirect, url_for, session, flash, make_response, send_file
from config.middlewares import is_doctor_logged_in
from config.DB import connect
import mysql.connector
import zipfile
import io,time

doctor = Blueprint("doctor", __name__)
# database config
DB = connect()
cursor = DB.cursor()


@doctor.route("/doctors")
def doctors_home():
    if(is_doctor_logged_in()):
        id = session['username']
        doctor_data = get_info(id)
        patients = get_patients(id)
        return render_template("doctors.html", patients=patients, doctor_data=doctor_data)
    else:
        return redirect("/")


# get all the patients that belongs to that doctor
def get_patients(doctor_id):
    patientsData = list()  # list of dicts (info per patient)
    getPatientsIds = "SELECT patient_id FROM `examine` WHERE doctor_id = %s" % (
        doctor_id,)
    cursor.execute(getPatientsIds)
    ids = cursor.fetchall()
    if(len(ids) == 0):
        return patientsData
    idsList = [id[0] for id in ids]
    # get the info of each id
    for id in idsList:
        getPatientInfo = "SELECT * FROM patients WHERE id = %s" % (id,)
        cursor.execute(getPatientInfo)
        info = cursor.fetchone()
        # create dict holds the data
        data = {
            'id' : info[2],
            'first_name': info[0],
            'last_name': info[1],
            'phone': info[4],
            'room_number': info[5],
            'email': info[8]
        }
        patientsData.append(data)
    # now i have all data i want
    return patientsData

# get doctor information


def get_info(doctor_id):
    get_doctor = "SELECT * FROM doctors WHERE id = %s" % (doctor_id)
    cursor.execute(get_doctor)
    info = cursor.fetchone()
    return {
        'firstName': info[0],
        'lastname': info[1],
        'phone': info[4],
        'department': info[5],
        'email': info[6]
    }


# update doctor info
@doctor.route('/doctors/updateInfo', methods=['GET', 'POST'])
def updat_doctor_info():
    if(request.method == "GET"):
        return redirect('/doctors')
    else:
        if is_doctor_logged_in():
            # code
            doctor_id = session['username']
            (firstName, lastName, phone, department, email) = (
                request.form['firstName'], request.form['lastName'], request.form['phone'], request.form['department'], request.form['email'])
            update_info = "UPDATE doctors SET fname = '%s', lname = '%s', phone = '%s', email = '%s', department = '%s' WHERE id = %s" % (
                firstName, lastName, phone, email, department, doctor_id)
            cursor.execute(update_info)
            DB.commit()
            flash('your info updated successfully')
            return redirect('/doctors')
        else:
            return redirect('/')

# update doctor password
@doctor.route('/doctors/updatePassword', methods=['GET', 'POST'])
def update_doctor_password():
    if(request.method == "GET"):
        return redirect('/doctors')
    else:
        if is_doctor_logged_in():
            # code
            doctor_id = session['username']
            oldPasswordForm = request.form['oldPassword']
            get_real_password = "SELECT password FROM doctors WHERE id = %s" % (
                doctor_id,)
            cursor.execute(get_real_password)
            realPassword = cursor.fetchone()[0]
            print(realPassword, oldPasswordForm)
            if realPassword == oldPasswordForm:
                # he is the real doc
                newPassword = request.form['newPassword']
                update_password = "UPDATE doctors SET password = %s WHERE id = %s" % (
                    newPassword, doctor_id)
                cursor.execute(update_password)
                DB.commit()
                flash("your password changed successfully")
                return redirect('/doctors')
            else:
                flash('the old password is incorrect')
                return redirect('/doctors')
            # return redirect('/doctors')

        else:
            return redirect('/')
        
# download patient scan
@doctor.route('/doctors/scans',methods=['GET','POST'])
def scans_Download():
    if(is_doctor_logged_in()) : 
        patient_id = request.args.get('patientId')
        if patient_id == None : return redirect('/doctors')
        get_scans = "SELECT patient_scan FROM scans WHERE patient_id = %s" % (
            patient_id)
        cursor.execute(get_scans)
        scansT = cursor.fetchall()
        scansList = [scan[0] for scan in scansT]
        if(len(scansList) != 0) : 
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                i = 1
                for binaryScan in scansList:
                    data = zipfile.ZipInfo("scan%s.jpg"%(i))
                    data.date_time = time.localtime(    time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, binaryScan)
                    i += 1
            memory_file.seek(0)
            return send_file(memory_file, attachment_filename='scans.zip', as_attachment=True)
        else : 
            flash("this patient doesn't have scans")
            return redirect('/doctors')
    else :
        return redirect('/')
        