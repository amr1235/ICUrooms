from flask import Blueprint,request,render_template,redirect,url_for, session
from datetime import timedelta
import mysql.connector
from routes.check import check

logIn = Blueprint("login",__name__)

DB = mysql.connector.connect(host="localhost",user="farook",passwd="sql123",database="ICUroomsDB")
cursor = DB.cursor()
@logIn.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST" :
        session.permanent = True
        return valid_login(request.form['id'],request.form['password'])
    else :
        return redirect("/") 

#get the id of the user returns -1 if it doesn't exist and returns the id if it exist
def getID(id) : 
    getid = "SELECT t.id FROM (SELECT id FROM doctors UNION SELECT id FROM patients UNION SELECT id FROM technicians) t WHERE id = %s"
    val = (id,)
    cursor.execute(getid,val)
    if cursor.fetchone() == None :
        return '-1'
    else :
        return id
# defining the id to know the user wheather he is a doctor or patien or tech it returns a object of id and the type
def defining_id (id) :
    idstr = str(id)
    lastTwoDigits = idstr[0] + idstr[1] # now i have the last two digits
    if lastTwoDigits == "00" :
        return {"id" : id, "typ" : 'doctors'}
    elif lastTwoDigits == "01" :
        return {"id" : id, "typ" : 'patients'}
    elif lastTwoDigits == "11" :
        return {"id" : id, "typ" : 'technicians'}
    else:
        return {"id" : id, "typ" : 'admins'}
    
# checkin if the id and the password is correct and log in if So
def valid_login(id,password) :
    error = ""
    ID = getID(id)
    if ID == '-1' :
        error = "this id doesn't exist "
        return render_template("index.html",error=error)
    else :
        idAndType = defining_id(id)
        # checking the password
        # get the password that belongs to that id (real password)
        getpass = "SELECT password FROM %s WHERE id = %s"%(idAndType['typ'],idAndType['id'])
        cursor.execute(getpass)
        realPassword = cursor.fetchone()[0]
        print(password , realPassword)
        if  realPassword == password : # somethin wrong here
            # assign a name to session
            session['username'] = request.form['id']
            return redirect('/%s'%(idAndType["typ"]))
        else : 
            error = "password incorrect"
            return render_template("index.html",error=error)
