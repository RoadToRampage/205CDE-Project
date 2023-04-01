from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



app = Flask(__name__)




app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testdrive'


mysql = MySQL(app)



@app.route('/', methods=['GET','POST'])
def home():
    error=''
    return render_template('Main.HTML',error='')


@app.route('/Test.HTML', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM logininfo WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            session.permanent = True
            return render_template('Browser.HTML',username=username)
        else:
            error = 'Invalid username and/or password'
    return render_template('Main.html', error=error)

@app.route('/Logout.HTML')
def Logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('password', None)
    return render_template('Main.HTML',error="Successfully Logged Out!")

@app.route('/Register.HTML', methods=['GET', 'POST'])
def Register():
    return render_template('Register.HTML',error="")

@app.route('/RegisterAccount.HTML',methods=['GET','POST'])
def RegisterAccount():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM logininfo WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            error="Account already exist"
            return render_template('Main.HTML',error=error)
        else:
            cursor.execute('INSERT INTO logininfo VALUES (%s, %s)', (username, password))
            mysql.connection.commit()
            error = 'Account has been successfully registered'
            return render_template('Main.HTML',error=error)
        
@app.route('/DataInput.HTML',methods=['GET','POST'])
def InputData():
    if 'username' in session:
        username = session['username']
    if request.method == 'POST':
        amethyst = request.form['amethyst']
        quartz = request.form['quartz']
        diamond = request.form['diamond']
        if amethyst:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer_wishlist WHERE username = %s AND purchasedItem = %s', (username, "amethyst"))
            data = cursor.fetchone()
            if data:
                cursor.execute('update customer_wishlist SET purchaseAmount = purchaseAmount + %s where purchasedItem = "amethyst"',(amethyst))
                mysql.connection.commit()
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO customer_wishlist (username,purchasedItem,purchaseAmount) VALUES (%s,%s,%s)', (username,"amethyst",amethyst))
                mysql.connection.commit()
        if quartz:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer_wishlist WHERE username = %s AND purchasedItem = %s', (username, "quartz"))
            data = cursor.fetchone()
            if data:
                cursor.execute('update customer_wishlist SET purchaseAmount = purchaseAmount + %s where purchasedItem = "quartz"',(quartz))
                mysql.connection.commit()
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO customer_wishlist (username,purchasedItem,purchaseAmount) VALUES (%s,%s,%s)', (username,"quartz",quartz))
                mysql.connection.commit()
        if diamond:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer_wishlist WHERE username = %s AND purchasedItem = %s', (username, "diamond"))
            data = cursor.fetchone()
            if data:
                cursor.execute('update customer_wishlist SET purchaseAmount = purchaseAmount + %s where purchasedItem = "diamond"',(diamond))
                mysql.connection.commit()
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO customer_wishlist (username,purchasedItem,purchaseAmount) VALUES (%s,%s,%s)', (username,"diamond",diamond))
                mysql.connection.commit()
        error = 'Successfully added to shopping cart!'
        return render_template('Browser.HTML',error=error,username=username)    

        
@app.route('/ShoppingCart.HTML')
def ShoppingCart():
    if 'username' in session:
        username=session['username']
        #cursor = mysql.connection.cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT purchaseAmount FROM customer_wishlist')
        cursor.execute('SELECT purchaseAmount FROM customer_wishlist WHERE username = %s AND purchasedItem = %s', (username, "amethyst"))
        amethystdata=cursor.fetchall()
        amethystdata_amount = int(amethystdata[0]["purchaseAmount"])
        amethysttotal=amethystdata_amount*320
        cursor.execute('SELECT purchaseAmount FROM customer_wishlist WHERE username = %s AND purchasedItem = %s', (username, "quartz"))
        quartzdata=cursor.fetchall()
        quartzdata_amount = int(quartzdata[0]["purchaseAmount"])
        quartztotal=quartzdata_amount*400
        cursor.execute('SELECT purchaseAmount FROM customer_wishlist WHERE username = %s AND purchasedItem = %s', (username, "diamond"))
        diamonddata=cursor.fetchall()
        diamonddata_amount = int(diamonddata[0]["purchaseAmount"])
        diamondtotal=diamonddata_amount*1000
        total=amethysttotal+quartztotal+diamondtotal
        return render_template('ShoppingCart.HTML',username=username,amethystdata=amethystdata_amount,quartzdata=quartzdata_amount,diamonddata=diamonddata_amount,amethysttotal=amethysttotal,quartztotal=quartztotal,diamondtotal=diamondtotal,total=total)
   
@app.route('/Browser.HTML')
def HomePage():
    if 'username' in session:
        username=session['username']
        return render_template('Browser.HTML',username=username)


if __name__ == "__main__":
    app.run(debug=True)