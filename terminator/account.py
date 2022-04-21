import functools

from flask import Blueprint, request, session, redirect, url_for, flash, render_template, g
from werkzeug.security import check_password_hash

from terminator.models import User

router = Blueprint('account', __name__, url_prefix='/account')


@router.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('maintenance-list'))

        flash(error)

    return render_template('account/login.html')


@router.route('/logout')
def logout():
    session.clear()
    return render_template('account/logout.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('account.login'))

        return view(**kwargs)

    return wrapped_view
