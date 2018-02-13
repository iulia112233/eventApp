from flask import render_template, request, g, url_for, redirect, flash, session, jsonify 
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy import create_engine, inspect
from app import app, db, lm
from .forms import LoginForm, RegistrationForm, EditForm
from models import User
from config import SQLALCHEMY_DATABASE_URI

@app.route('/')
@app.route('/index')
def index():
 if not session.get('user'):
    return redirect(url_for('login'))
 else:   
    return render_template('index.pug')

@app.route('/login', methods = ['GET'])
def login():
    return render_template('login.pug')

@app.route('/register', methods = ['GET'])
def g_register(): 
   return render_template('register.pug')

@app.route('/logout', methods = ['GET'])
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    if not session.get('user'):
        return render_template('login.pug')
    return render_template('edit.pug')

@app.route('/changePicture', methods = ['GET'])
def change_picture():
    if not session.get('user'):
        return render_template('login.pug')
    return render_template('gallery.pug')

@app.route('/manageUsers', methods = ['GET'])
def manage_users():
    if not session.get('user'):
        return render_template('login.pug')
    if session.get('user')['role'] != 'admin':
        return render_template('login.pug')
    return render_template('/manageusers.pug')    

@app.route('/reset', methods = ['GET'])
def reset_password():
    t = request.args.get('token')
    if t:
        user = User()
        v = user.verifyToken(t)
        user.username = v
        if user.exists():
            return render_template('resetPassword.pug', username = v)
        else:
            flash('Username does not exist!')
            render_template('reset.pug')
    return render_template('reset.pug')   

@app.route('/event', methods = ['GET'])
def view_event():
    return render_template('event.pug')

@app.route('/order', methods =['GET'])
def view_order():
    return render_template('order.pug')

@app.route('/order-complete', methods = ['GET'])
def view_order_complete():
    return render_template('order-complete.pug')

