from flask import Blueprint, redirect, render_template, session
from routes.check import check

ad = Blueprint('admin' ,__name__)

@ad.route('/admin')
def admin_home():
    if check() == 'admin' :
        return 'Admin Page'
    return 'not admin'
