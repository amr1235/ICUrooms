from flask import Blueprint,request,render_template,redirect,url_for, session
from config.middlewares import is_doctor_logged_in

doctor = Blueprint("doctor",__name__)

@doctor.route("/doctors")
def doctors_home():
    if(is_doctor_logged_in()) :
        return "hi Doc "
    else : 
        return redirect("/")
    
    