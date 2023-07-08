import sys

from . import auth
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.User import User
from app.extensions import db
from app.forms.login import LoginForm, RegisterFrom, ChangePasswordForm
from datetime import datetime
import app


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        # get user by email
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if user.verify_password(form.password.data):
                if not user.lock:
                    # login & redirect
                    login_user(user) # can add remember me

                    # update last seen
                    user.last_seen = datetime.utcnow()
                    db.session.add(user)
                    db.session.commit()

                    return redirect(request.args.get('next') or url_for('index'))
                else:
                    flash('Your account is locked')
            else:
                flash('Password Input Error!!!')
        else:
            flash('Email does not exist!!!')

        return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterFrom()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        # check identity of email & username
        if User.query.filter_by(username=username).first():
            flash('The Username is registered, please change a new Username.')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('The Email is registered, please change a new Email Address.')
            return redirect(url_for('auth.register'))

        # register
        user = User(
            username=username,
            email=email,
            password=form.password.data,
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            birthday = form.birthday.data,
            is_married = form.is_married.data,
            share = form.share.data
        )

        db.session.add(user)
        db.session.commit()

        flash('Successfully registered! Please log in')

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/change_pwd', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        # verify old password
        if current_user.verify_password(form.oldPassword.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()

            flash('Password was changed successfully!')
            return redirect(url_for('index'))

    return render_template('change_password.html', form=form)