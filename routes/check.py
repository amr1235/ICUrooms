# check for sessions and user validation
from flask import session, redirect, render_template
# from app import Id

def check():
    if 'username' in session :
        userid = session['username']     
        lastTwoDigits = userid[len(userid) - 2] + userid[len(userid) - 1] # now i have the last two digits
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

