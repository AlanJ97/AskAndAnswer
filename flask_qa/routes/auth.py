from flask import Blueprint, render_template, request, redirect, url_for
from ..extensions import db
from ..models import User
from werkzeug.security import check_password_hash
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    print("jhkjhkjh")
    if request.method == 'POST':
        print("entra")
        name = request.form['name']
        unhashed_password = request.form['password']
        print(name, unhashed_password)
        user = User(
            name = name, 
            unhashed_password = unhashed_password, 
            admin = True, 
            expert = False
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name = name).first()
        error_message = ''
        if not user or not check_password_hash(user.password, password):
            error_message = 'Try again, it failed'
        if not error_message:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html')