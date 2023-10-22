from flask import Flask,redirect,render_template,url_for,request,session,flash
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
import re
import base64

app=Flask(__name__)
app.secret_key='ewwugwduiscgwgf'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='kogkurgat@gmail.com'
app.config['MAIL_PASSWORD']='ayfdzpbglzqkebop'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='shop'
app.config["MYSQL_CHARSET"]='latin1'

mysql=MySQL(app)




@app.route('/register',methods=['POST','GET'])
def register(): 
    if request.method=='POST' :
        username=request.form['name']
        email=request.form['email']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO register(username,email,password) values(%s,%s,%s)",(username,email,password,))
        mysql.connection.commit()
        cur.close()
        msg=Message(subject='Account creation',sender="kogkurgat@gmail.com",recipients=[email])
        msg.body=f"""Welcome to Tobby's shop
                    Your account credentials are
                    username:{username}
                    password:{password}
                    You can now order you goods an service from our website"""
        try:
            mail.send(msg)
        except Exception as error:
            return error
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM register WHERE username=%s AND password=%s",(username,password))
        mysql.connection.commit()
        data=cur.fetchone()
        if data:
            session['id']=data[0]
            session['username']=data[1]
            session['email']=data[2]
            session['password']=data[3]
            flash(f" Your have logged in as {username}","success")
            return redirect(url_for("home"))
        else:
            flash(f"Your have entered the wrong credential")
            return render_template("login.html",username=username,password=password)
    return render_template('login.html')


@app.route('/forgotpassword', methods=['POST','GET'])
def forgotpassword():
    if request.method=='post':
        email=request.form['email']
        
    return render_template('forgotpassword.html')
 
@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('id',None)
    session.pop('password',None)
    session.pop('email',None)
    flash(f"Your logged out successfully")
    return redirect('login')
 
 
@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/profile',methods=['POST','GET'])
def profile():
    
    return render_template('profile.html')
  
@app.route('/')
def home():
    cur=mysql.connection.cursor()
    cur.execute("SELECT  * FROM products")
    data= cur.fetchall()
    all_data=[]
    for item in data:
        img=item[1]
        image=base64.b64encode(img).decode('utf-8')
        all_items=list(item)
        all_items[1]=image
        all_data.append(all_items)
    cur.close()
    return render_template ('home.html',all_data=all_data)
    return render_template("home.html")

@app.route('/product',methods=['POST','GET'])
def product():
    if request.method=='POST':
        pic=request.files['pic']
        price=request.form['price']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO products(pic,price) values(%s,%s) ",(pic.read(),price,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    return render_template("product.html")

if __name__=='__main__':
    app.run(debug=True)