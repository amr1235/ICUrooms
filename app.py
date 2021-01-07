from flask import Flask
from datetime import timedelta
from routes.login import logIn
import mysql.connector

app = Flask(__name__)
app.secret_key = b'ad^&%#HJaS54O%$%' # to encrypte the data
app.permanent_session_lifetime = timedelta(days=5) # 5-day session
app.register_blueprint(logIn)

@app.route('/')   
def index():
    # if the session exists
    if 'username' in session:
        return render_template('index.html')
    else: 
        return render_template('loginForm.html')

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
