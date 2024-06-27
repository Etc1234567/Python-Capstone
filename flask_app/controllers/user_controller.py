from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models import user_model
from flask_app.models import vacation_model
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if "user_id" in session:
       return redirect('/dashboard')
    return render_template("loginreg.html")

@app.route('/dashboard')
def render_dashboard():
    if "user_id" not in session:
        return redirect("/")
    
    logged_user = user_model.User.get_by_id({"id": session['user_id']})
    
    vacations = vacation_model.Vacation.get_all()

    return render_template("dashboard.html", vacations=vacations, logged_user=logged_user)

@app.route('/register', methods=['POST'])
def register():
    if not user_model.User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password" : pw_hash,
        "confirm" : pw_hash
    }

    user_id = user_model.User.save(data)

    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    
    potential_user = user_model.User.get_by_email(request.form)
    
    if not potential_user:
        flash("Invalid Email/Password", 'log')
        return redirect("/")
    
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash("Invalid Email/Password", 'log')
        return redirect('/')
    
    session['user_id'] = potential_user.id

    return redirect("/dashboard")

@app.route("/logout")
def log_out():
    del session['user_id']
    return redirect("/")