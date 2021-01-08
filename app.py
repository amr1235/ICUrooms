from flask import Flask,session,render_template, redirect
from datetime import timedelta
from routes.login import logIn
from routes.tech import tech
from routes.admin import ad
from routes.check import check
import mysql.connector

app = Flask(__name__)
app.secret_key = b'ad^&%#HJaS54O%$%' # to encrypte the data
app.permanent_session_lifetime = timedelta(days=5) # 5-day session
app.register_blueprint(logIn)
app.register_blueprint(ad)#, url_prefix='/admin')
app.register_blueprint(tech, url_prefix='/tech')

Id = 0 # global variable for session['username']


@app.route('/')   
def index():
    # if the session exists
    if 'username' in session:
        user = check()
        return redirect(f'/{user}/')
    else: 
        return render_template('index.html')

@app.route('/logout')   
def logout():
    # if the session exists
    if 'username' in session:
        session.pop('username', None) # remove the session
        return 'logged out'
    else: 
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/doctor/')   # this function is just for testing until you create file for doctors 
def doc():
    # if the session exists
    if check() == 'doctor':
        return 'doctoooooooor'
    else: 
        return 'not doooooooc'