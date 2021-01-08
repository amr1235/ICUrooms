from flask import Blueprint, redirect, render_template, session
from routes.check import check

tech = Blueprint('tech' , __name__)

@tech.route('/')
def tech_home():
    if check() == 'tech':
        return '<h1>technician</h1>'
    else:
        return 'not tech'

