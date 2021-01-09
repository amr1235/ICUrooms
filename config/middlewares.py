from flask import session 


#middleware to check if there is a user is logged in 
def is_logged_in() :
    if 'username' in session : 
        return True 
    else :
        return False

#middleware to check if there is a doctor is logged in 
def is_doctor_logged_in():
    if(is_logged_in()) :
        session['username'][0] + session['username'][1]
        if((session['username'][0] + session['username'][1]) == "00"):
            return True
        else : 
            return False
    else :
        return False
    

