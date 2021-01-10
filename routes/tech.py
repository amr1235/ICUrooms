from flask import Blueprint, redirect, render_template, session, request
from routes.check import check

tech = Blueprint('tech' , __name__)

@tech.route('/')
def tech_home():
    data = request.form['device']
    # if check() == 'tech':
    #     if request.form['id'] == session['username']:
    #         data = request.form
    return data#'<h1>technician <br> {{ data }}</h1>'
    # else:
    #     return 'not tech'

