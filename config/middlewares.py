from flask import session 
from routes.check import check

#middleware to check if there is a user is logged in 
def is_logged_in() :
    if 'username' in session : 
        return True 
    else :
        return False

#middleware to check if there is a doctor is logged in 
def is_doctor_logged_in():
    if(is_logged_in()) :
        idstr = str(session['username'])
        lastTwoDig = idstr[len(idstr) - 2] + idstr[len(idstr) - 1]
        if(lastTwoDig == "00"):
            return True
        else : 
            return False
    else :
        return False

#middleware to check if there is a patient is logged in 
def is_patient_logged_in():
    if is_logged_in() :
        if check() == 'patients' :
            return True 
        else : 
            return False
    else :
        return False
