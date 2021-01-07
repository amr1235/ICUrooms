from flask import Blueprint,request,render_template,redirect,url_for
import mysql.connector
logIn = Blueprint("login",__name__)

DB = mysql.connector.connect(host="localhost",user="root",passwd="mysql",database="ICUroomsDB")
cursor = DB.cursor()
@logIn.route('/login',methods=['GET','POST'])
def login():
    error=""
    if request.method == "POST" :
        return valid_login(request.form['id'],request.form['password'])
    else :
        return render_template("loginForm.html",error=error) 

#get the id of the user returns -1 if it doesn't exist and returns the id if it exist
def getID(id) : 
    getid = "SELECT t.id FROM (SELECT id FROM doctors UNION SELECT id FROM patients) t WHERE id = %s"
    val = (id,)
    cursor.execute(getid,val)
    if cursor.fetchone() == None :
        return -1
    else :
        return id
# defining the id to know the user wheather he is a doctor or patien or tech it returns a object of id and the type
def defining_id (id) :
    idstr = str(id)
    lastTwoDigits = idstr[len(idstr) - 2] +  idstr[len(idstr) - 1] # now i have the last two digits
    if lastTwoDigits == "00" :
        return {'id' : id, 'typ' : "doctors"}
    elif lastTwoDigits == "01" :
        return {'id' : id, 'typ' : "patients"}
    else :
        return {'id' : id, 'typ' : "technicians"}
    
# checkin if the id and the password is correct and log in if So
def valid_login(id,password) :
    error = ""
    ID = getID(id)
    if ID == -1 :
        error = "this id doesn't exist "
        return render_template("loginForm.html",error=error)
    else :
        idAndType = defining_id(id)
        # checking the password
        # get the password that belongs to that id (real password)
        getpass = "SELECT PASSWORD FROM %s WHERE id = %s"%(idAndType['typ'],int(idAndType['id']))
        cursor.execute(getpass)
        realPassword = cursor.fetchone()[0]
        if (realPassword == password) : 
            # authintication correct and making seasion
            print("correct")
            return render_template("loginForm.html",error=error)
        else : 
            error = "password incorrect"
            return render_template("loginForm.html",error=error)
        
    
    
    
    
    
