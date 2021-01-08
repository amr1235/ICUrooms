from flask import Blueprint, redirect, render_template, session
from routes.check import check
ad = Blueprint('admin' ,__name__)

@ad.route('/')
def admin_home():
    user_typ = check()
    return 'Admin Page'
