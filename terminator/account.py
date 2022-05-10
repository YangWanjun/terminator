from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import check_password_hash

from terminator.models import User
from terminator.utils import constant
from terminator.utils.cas import cas_verify_ticket

router = Blueprint('account', __name__, url_prefix='/account')

login_manager = LoginManager()


def init_login_manager(app):
    with app.app_context():
        login_manager.init_app(app)


@router.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    is_gmail_login = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = constant.ERROR_INVALID_CREDENTIALS
        elif not check_password_hash(user.password, password):
            error = constant.ERROR_INVALID_CREDENTIALS

        if error is None:
            login_user(user)
            return redirect(url_for('maintenance-list'))

        flash(error)
    elif request.method == 'GET':
        ticket = request.args.get('ticket')
        if ticket:
            # CASログイン
            username = cas_verify_ticket(ticket)
            user = User.query.filter_by(username=username).first()
            if user is None:
                error = constant.ERROR_CAS_INVALID_USER
            if error is None:
                login_user(user)
                return redirect(url_for('maintenance-list'))
            is_gmail_login = True
            flash(error)

    return render_template('account/login.html', is_gmail_login=is_gmail_login)


@router.route('/logout')
def logout():
    logout_user()
    return render_template('account/logout.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/account/login')
