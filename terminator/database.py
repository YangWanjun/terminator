import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def init_app(app: Flask) -> None:
    db.init_app(app)
    app.cli.add_command(drop_tables_command)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_user)


@click.command('drop-tables')
@with_appcontext
def drop_tables_command():
    import terminator.models
    db.drop_all(bind=None)
    click.echo('All table dropped.')


@click.command('init-db')
@with_appcontext
def init_db_command():
    import terminator.models
    db.create_all(bind=None)
    click.echo('Initialized the database.')


@click.command('create-user')
@with_appcontext
def create_user():
    username = click.prompt('ユーザー名を入力してください', type=str)
    email = click.prompt('メールアドレスを入力してください', type=str)

    def read_password():
        return (
            click.prompt('パスワードを入力してください', hide_input=True, type=str, default=""),
            click.prompt('パスワード（確認）を入力してください', hide_input=True, type=str, default=""),
        )

    password, password_confirm = read_password()
    while password != password_confirm:
        click.secho('パスワードが不一致です、もう一回ご入力ください', fg='red')
        password, password_confirm = read_password()

    from .models import User
    user = User(username=username, email=email)
    if password:
        user.password = generate_password_hash(password)
    else:
        user.password = ""
    try:
        db.session.add(user)
        db.session.commit()
        click.echo(f'ユーザー「{user.id}:{username}」は追加しました.')
    except IntegrityError:
        click.secho('既に存在しているユーザーです。', fg='red')
