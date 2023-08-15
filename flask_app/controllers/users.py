from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def home():
    return render_template('register.html')

@app.route('/register/process', methods=['POST'])
def register():
    if not user.User.validate_register(request.form):
        return redirect('/register')
    print("-------------------------")
    print(request.form)
    pw_hash=bcrypt.generate_password_hash(request.form['password'])
    user_info={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    session['user_id']= user.User.save_user(user_info)
    id=session['user_id']
    session['first_name'] = user_info['first_name']
    return redirect('/dashboard')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_process', methods=['POST'])
def login_process():
    user_info=user.User.get_user_by_email(request.form)
    if not user_info:
        flash("Invalid Email !","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_info.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login')
    session["user_id"] = user_info.id
    session["first_name"] = user_info.first_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')