from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
# from flask_mongoengine import MongoEngine
# import json
import mysql.connector

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root1234",
  auth_plugin='mysql_native_password',
  database = 'products'
)

mycursor = mydb.cursor()

@app.route('/', methods=['GET'])
def index():
    resp = ""
    try:
        mycursor.execute("select * from product")#Execute SQL Query to selects all record
        result=mycursor.fetchall() #fetches all the rows in a result set
        for i in result:
            resp += str(i[0]) + "\t" + i[1] + "\t" + i[2] + "\n"
        print(resp) 
        return resp
    except(error):  
        print(error)
        return "Error:Unable to fetch data."

@app.route('/create', methods=['POST'])
def create():
    try:
        request_data = request.get_json()
        id1 = request_data['id']
        name = request_data['productname']
        cost = request_data['cost']
        print( id1, name, cost)
        sql = "INSERT INTO product(id, productname, price) VALUES(%s,%s, %s)"
        data = (id1,name, cost)
        mycursor.execute(sql, data)
        mydb.commit() # Commit is used for your changes in the database  
        print('Record inserted successfully...')
        return 'Record inserted successfully...'
    except:  
        # rollback used for if any error   
        mydb.rollback() 
        return "Error"

@app.route("/delete", methods=["DELETE"])
def delete():
    id1 = request.args.get('id')
    try:   
        mycursor.execute("DELETE FROM product WHERE id=%s", (id1,))#Execute SQL Query to detete a record   
        mydb.commit() # Commit is used for your changes in the database  
        print('Record deteted successfully...')
        return 'Record deteted successfully...'
    except:  
        # rollback used for if any error  
        mydb.rollback()  
        return 'Error'

@app.route("/update", methods=["PATCH"])
def update():
    request_data = request.get_json()
    id1 = request.args.get('id')
    name = request_data['productname']
    price = request_data['cost']
    print(id1, name, price)
    try:
        sql = "UPDATE product SET productname=%s, price=%s WHERE id=%s"
        data = (name, price, id1,)
        mycursor.execute(sql, data)
        mydb.commit()
        print('Record updated successfully...') 
        return 'Record updated successfully...'
    except:   
    # rollback used for if any error  
        mydb.rollback()
        return "Error"