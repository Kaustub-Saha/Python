# importing Flask and other modules
from flask import Flask, request, render_template, session
import pymysql
from basic import mysqlconnect 
import sys
  
# Flask constructor
app = Flask(__name__)   

#Creating a connection to the database
conn = pymysql.connect(
        host='localhost',
        user=<Username of your Database>, 
        password = <Password of your Database>,
        db='intdb',
        )

#This method is used to insert data into the database
@app.route('/insertdata', methods =["GET", "POST"])
def insertdata():
    if request.method == "POST":
       first_name = request.form["firstname"]
       last_name = request.form["lastname"]
       Phone_No = request.form["phoneno"]
       sex = request.form["sex"]
       Race = request.form["race"]
       DOB = request.form["dob"]
       St_Address = request.form["st_address"]
       City = request.form["city"]
       County = request.form["county"]
       State = request.form["state"]
       Zipcode = request.form["zipcode"]
       Email = request.form["email"]
       Password = request.form["password"]
       print("arguements received")
       cur = conn.cursor()
       cur.execute("INSERT INTO client(fname,lname,phone_no,sex,race,dob,St_Address, City, County, State, Zipcode, Email, Password) VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(first_name,last_name,Phone_No,sex,Race,DOB,St_Address,City,County,State,Zipcode,Email,Password))
       conn.commit()
       cur.close()
    return render_template("index.html")

#To present the data in a Tabular format
@app.route('/viewdata')
def show():
    cur = conn.cursor()
    resultValue = cur.execute("select fname,lname,st_address,zipcode,city,county,state,phone_no,email from client where cid IN (select cid from test, client where clientid = cid and result = 'Positive')")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('name.html',userDetails=userDetails)
  
if __name__=='__main__':
   app.run(debug = True)
