import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root1234",
  auth_plugin='mysql_native_password',
  database = 'products'
)

mycursor = mydb.cursor()

# mycursor.execute("create database products")

mycursor.execute("create table product(id INT,productname VARCHAR(255),price VARCHAR(255))")

# mycursor.execute("show databases")

# for i in mycursor:
#   print(i)
mydb.close()#Connection Close  