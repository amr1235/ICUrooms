from flask import Flask,render_template
from routes.login import logIn
import mysql.connector

app = Flask(__name__)
app.register_blueprint(logIn)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
