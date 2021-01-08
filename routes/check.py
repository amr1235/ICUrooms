# check for sessions and user validation
from flask import session, redirect, render_template
from routes.login import Id

def check():
    if 'username' in session :
        session['username'] = userid   
        lastTwoDigits = userid[len(userid) - 2] + userid[len(userid) - 1] # now i have the last two digits
        if lastTwoDigits == "00" :
            return 'doctor'
        elif lastTwoDigits == "01" :
            return 'patient'
        elif lastTwoDigits == "10" : 
            return 'tech'
        elif lastTwoDigits == "11" :
            return 'admin' 

