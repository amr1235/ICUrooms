# check for sessions and user validation
from flask import session, redirect, render_template
# from app import Id

def check():
    if 'username' in session :
        id = session['username']     
        str_id = str(id)
        lastTwoDigits = str_id[len(str_id) - 2] + str_id[len(str_id) - 1] # now i have the last two digits
        if lastTwoDigits == "00" :
            return 'doctors'
        elif lastTwoDigits == "01" :
            return 'patient'
        elif lastTwoDigits == "11" : 
            return 'tech'
        elif lastTwoDigits == "10" :
            return 'admin' 
        else:
            return 'not in users'

def userType(id):
    str_id = str(id)
    lastTwoDigits = str_id[len(str_id) - 2] + str_id[len(str_id) - 1] # now i have the last two digits
    if lastTwoDigits == "00" :
        return 'doctors'
    elif lastTwoDigits == "01" :
        return 'patients'
    elif lastTwoDigits == "11" : 
        return 'technicians'
    elif lastTwoDigits == "10" :
        return 'admins' 
    else:
        return 'not in users'
