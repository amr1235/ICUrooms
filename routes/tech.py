from flask import Blueprint, redirect, render_template, session

tech = Blueprint('tech' , __name__)

@tech.route('/technician')
def tech_home():
    if # technician?
        return '<h1>technician</h1>'
    else:
        #error

