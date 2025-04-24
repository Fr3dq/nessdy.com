from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .security import StrongPasswordVeryfication, ResetPasswordToken, SendEmail

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        verified = user.verified

        if user and verified == "yes":
            if  check_password_hash(user.password, password):
                flash('You are logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            if verified != "yes":
                flash('Account not vefified. Contact us', category='error')
            flash('Email does not exist', category='error')

   return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get("firstName")
        name_surname = request.form.get('Name_surname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        username = User.query.filter_by(first_name=first_name).first()

        if user:
            flash('Email already exists', category='error')
        elif username:
            flash('Username already exists', category = 'error')
        elif len(email) < 3:
            flash('Email is too short', category='error')
        elif len(first_name) < 2:
            flash('First name is too short', category='error')
        elif password1 != password2:
            flash('Password do not match', category='error')
        elif StrongPasswordVeryfication(password1) == 1:
            flash('Password is too short or do not contain special character (#...)', category='error')
        else:
            sing_up_token = ResetPasswordToken() * 10
            new_user = User(email=email, first_name=first_name, name_surname = name_surname, password = generate_password_hash(password1, method='pbkdf2:sha256'), verified=sing_up_token)
            db.session.add(new_user)
            db.session.commit()
            SendEmail(email, sing_up_token, 2)
            return redirect(url_for('auth.verify', user_email=new_user.email))

    return render_template("sign_up.html", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='error')
    return redirect(url_for('auth.login'))

@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    email = request.form.get("email")
    user_email = User.query.filter_by(email=email).first()
    
    if user_email is not None:
        token = ResetPasswordToken()
        user_email.token = token
        db.session.commit()
        SendEmail(email, token, 1)
        return redirect(url_for('auth.token', email=email))
    else:
        flash("Email does not exist", category="error")
        return render_template("password.html", user=current_user)

@auth.route('/token', methods=['GET', 'POST'])
def token():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first() if email else None

    if request.method == 'POST':
        entered_token = int(request.form.get('code'))
        password = request.form.get('password')
        passwordR = request.form.get('password1')

        if user.token == entered_token:
            if password != passwordR:
                flash("Password do not match", category='error')
            elif StrongPasswordVeryfication(password) == 1:
                flash('Password is too short or do not contain special character (#...)', category='error')
            else:
                user.password = generate_password_hash(passwordR, method='pbkdf2:sha256')
                user.token = ResetPasswordToken() * 10
                db.session.commit()
                flash('succes', category='error')
                return render_template("home.html", user=current_user)
        else:
            flash('Invalid code', category='error')

    return render_template("token.html", user=current_user)

@auth.route('/verify', methods=['GET', 'POST'])
def verify():   
    if request.method == 'POST':
        try:
            user_email = request.args.get('user_email')
            user = User.query.filter_by(email=user_email).first()
            code = request.form.get('verify')
            if code == user.verified: 
                user.verified = "yes"
                db.session.commit()
                login_user(user, remember=True)
                flash('Account created', category='success')
                return redirect(url_for('views.facts'))
            else:
                flash('Incorrect code', category='success')
        except:
            flash('We are sorry. Contact us', category='success')

    return render_template("verify.html", user=current_user) 