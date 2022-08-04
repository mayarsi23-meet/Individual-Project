from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  "apiKey": "AIzaSyCHD4d7i2_l1yFBxKUqM_QWGpx9nmu9QI4",
  "authDomain": "individualproject-bdb55.firebaseapp.com",
  "projectId": "individualproject-bdb55",
  "storageBucket": "individualproject-bdb55.appspot.com",
  "messagingSenderId": "1024080929004",
  "appId": "1:1024080929004:web:3fb2002385af1b5c2305c9",
  "measurementId": "G-XZ4GEYH7MR",
  "databaseURL":"https://individualproject-bdb55-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase= pyrebase.initialize_app(config)
auth=firebase.auth()
db= firebase.database()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/men')
def men():
    return render_template("men.html")

@app.route('/women')
def women():
    return render_template("women.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user']=auth.create_user_with_email_and_password(email,password)
        users={"email":request.form['email'], "password":request.form['password'], "firstname": request.form['first_name'], "lastname": request.form['last_name'], "username": request.form['username'], "birthdate": request.form['birthdate']}
        db.child("Users").child(login_session['user']['localId']).set(users)
        try:
            return redirect(url_for('index'))
        except:
            error="Authentication failed"
        return render_template("signup.html", error="error")
    return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('index'))
        except:
            return render_template("signin.html", error = "Sign in failed")
    else:
        return render_template("signin.html")


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)