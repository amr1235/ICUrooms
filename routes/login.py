from flask import Blueprint

logIn = Blueprint("login",__name__)

@logIn.route('/login')
def login():
    return "login Form"

