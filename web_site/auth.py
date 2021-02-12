from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .models import User, data_base
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login_page.html')
    else:
        email = request.form['email']
        password = request.form['password']
        loaded_user = User.query.filter_by(email=email).first()
        if loaded_user:
            if check_password_hash(loaded_user.password, password):
                login_user(loaded_user, remember=True)
                flash('logged in successfully', 'succes')
                return redirect(url_for('home.home_page'))
        flash('email or password are incorrect', 'error')
        return render_template('login_page.html')

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash('logged out successfully', 'success')
    return redirect(url_for('home.home_page'))

@auth.route('/registration', methods= ['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registr_page.html')
    else:
        email = request.form['email']
        user_name = request.form['user_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email_in_database = User.query.filter_by(email=email).first()
        if email_in_database:
            flash('Email already exists', 'error')
            return render_template('registr_page.html')
        if len(user_name) < 4 or len(user_name) > 20:
            flash('Username incorrect. Must longer than 3 and shorter than 20', 'error')
            return render_template('registr_page.html')
        if len(password1) < 4 or len(password1) > 20:
            flash('Password incorrect. Must longer than 3 and shorter than 20', 'error')
            return render_template('registr_page.html')
        if password1 != password2:
            flash('Passwords are not match', 'error')
            return render_template('registr_page.html')

        user_to_database = User(email=email,
                                name=user_name,
                                password=generate_password_hash(password1, method='sha256'),
                                first_name='',
                                last_name='')
        data_base.session.add(user_to_database)
        data_base.session.commit()
        flash('You have signed up successfully', 'success')
        return redirect(url_for('home.home_page'))