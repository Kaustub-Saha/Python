#importing packages
import os
from django.core.files.storage import FileSystemStorage
import pymysql
import datetime
import pyqrcode
from pyqrcode import QRCode
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
global username

#This is the home page of the application
def index(request):
    if request.method == 'GET':
#When we suffix the URL with index.html. It takes us to the home page
       return render(request, 'index.html', {})

#this function renders the admin login html page
def AdminLogin(request):
# We use the Get method here
    if request.method == 'GET':
#Upon clicking the admin log in page is rendered
       return render(request, 'AdminLogin.html', {})

#This method is responsible for admin login action
def AdminLoginAction(request):
    global username
    #we use post method here as we are connecting with the server
    if request.method == 'POST':
    #Admin uses a preset user id and password to log in
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
    #the Admins username and password is set here 
    # we have two sets of admin userids for the admins to log in
        if username == 'admin1' and password == 'admin1':
    #we now check if the usernames are in accordance with that we have set.
    #if it is same as that we have set, the admins are good to log in 
            context= {'data':'Welcome Admin'}
            return render(request, 'AdminScreen.html', context)
    #This is another choice of admin user id and password that the admin can use
        elif username == 'administrator' and password == 'administrator':
            context= {'data':'Welcome Admin'}
            return render(request, 'AdminScreen.html', context)
    #if the password and userid of the admin does not match the log in fails 
        else:
            context= {'data':'login failed. Please retry'}
            return render(request, 'AdminLogin.html', context)  

#This is the method that renders the add employee page
def AddEmp(request):
    if request.method == 'GET':
#This page contains all the details about the details that the admin needs to enter for the user details
       return render(request, 'AddEmp.html', {})

#This code renders the user login page
def UserLogin(request):
    if request.method == 'GET':
#The user selects his or her id and clicks on login button 
       return render(request, 'UserLogin.html', {})  

def test(request):
    if request.method == 'GET':
       return render(request, 'test.html', {})

#View Employee attendance method is used to check the attendance of a particular employee
def ViewEmpAttendanceAction(request):
    if request.method == 'POST':
        #We fetch the employee id and start and end date entered by the admin
        empid = request.POST.get('t1', False)
        from_date = request.POST.get('t2', False)
        to_date = request.POST.get('t3', False)
        #We take the string format of the start and end date
        from_dd = str(datetime.datetime.strptime(from_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        to_dd = str(datetime.datetime.strptime(to_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        #we create the columns that we would like to see for the user attendance table
        columns = ['Employee ID', 'Presence Date']
        #we shape the table in this section
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        #We iterrate over the columns 
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        #we Create a connection with the mysql database that is stored in the local system
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from mark_attendance where employeeID='"+empid+"' and attended_date between "+from_dd+" and "+to_dd)
            rows = cur.fetchall()
            for row in rows:
                presence_days = presence_days + 1
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td></tr>"
        
        context= {'data': output}
        print(rows)
        query = "select * from mark_attendance where employeeID='"+empid+"' and attended_date between "+from_dd+" and "+to_dd
        df = pd.read_sql(query, con)
        filename = empid+'_'+str(datetime.datetime.now().date())
        df.to_csv("EmployeeAttendance/attendance_data/"+filename+'.csv')
        return render(request, 'AdminScreen.html', context)

def ViewEmpAttendance(request):
    if request.method == 'GET':
        font = '<font size="" color="black">'
        output = '<tr><td>'+font+'Choose&nbsp;Emp ID</td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select employeeID FROM employee_details")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+row[0]+'">'+row[0]+'</option>'
        output += "</select></td></tr>"
        context= {'data1': output}
        return render(request, 'ViewEmpAttendance.html', context)

def ViewAttendance(request):
    if request.method == 'GET':
        return render(request, 'ViewAttendance.html', {})

def ViewAttendanceAction(request):
    if request.method == 'POST':
        global username
        empid = username
        from_date = request.POST.get('t1', False)
        to_date = request.POST.get('t2', False)
        from_dd = str(datetime.datetime.strptime(from_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        to_dd = str(datetime.datetime.strptime(to_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        presence_days = 0
        salary = 0
        columns = ['Emp ID', 'Attended Date']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        # con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
        # with con:
        #     cur = con.cursor()
        #     cur.execute("select emp_salary FROM employee_details where employeeID='"+empid+"'")
        #     rows = cur.fetchall()
        #     for row in rows:
        #         salary = row[0]
        #         break
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from mark_attendance where employeeID='"+empid+"' and attended_date between "+from_dd+" and "+to_dd)
            rows = cur.fetchall()
            for row in rows:
                presence_days = presence_days + 1
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td></tr>"
        # output += "<tr><td>"+font+"Attended Days : "+str(presence_days)+"</font><td>"+font+"Current Salary = "+str(((salary/30) * presence_days))+"</td></tr>"        
        context= {'data': output}
        return render(request, 'UserScreen.html', context)    

def ViewEmp(request):
    if request.method == 'GET':
        
        columns = ['Emp ID', 'Name', 'Phone No', 'Designation']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM employee_details")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"
                output += "<td>"+font+str(row[3])+"</td>"
        context= {'data': output}
        return render(request, 'AdminScreen.html', context)

def UserLoginAction(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        index = 0
        emp_name = None
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select employeeID, empployeeName FROM employee_details")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    emp_name = row[1]
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+emp_name}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed. Please retry'}
            return render(request, 'UserLogin.html', context)        

def DownloadAction(request):
    if request.method == 'POST':
        global username
        infile = open("EmployeeAttendance/static/qrcodes/"+username+".png", 'rb')
        data = infile.read()
        infile.close()       

        response = HttpResponse(data, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=%s' % username+".png"
        return response

def AddEmpAction(request):
    if request.method == 'POST':
        global username
        ids = request.POST.get('t1', False)
        name = request.POST.get('t2', False)
        phone = request.POST.get('t3', False)
        desg = request.POST.get('t4', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select employeeID FROM employee_details")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == ids:
                # if row[0] == empid:
                    output = ids+" employee already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'emp_attendance',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO employee_details(employeeID,empployeeName,phoneNo,designation) VALUES('"+ids+"','"+name+"','"+phone+"','"+desg+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            url = pyqrcode.create(ids)
            url.png('EmployeeAttendance/static/qrcodes/'+ids+'.png', scale = 6)
            username = ids
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'Emp Details Saved with ID : '+ids
        context= {'data':output}
        return render(request, 'Download.html', context)
      


