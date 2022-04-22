from functools import wraps

from flask import session, g

from terminator.database import db
from terminator.models import User


def register_hooks(app):
    """Register hooks."""

    @app.before_request
    def before_request():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = User.query.filter_by(id=user_id).first()


def transaction(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if db.session.info.get('in_transaction') is True:
            return func(*args, **kwargs)
        else:
            db.session.info['in_transaction'] = True
            try:
                results = func(*args, **kwargs)
                db.session.commit()
                return results
            except Exception as ex:
                db.session.rollback()
                raise ex
            finally:
                db.session.info['in_transaction'] = False
    return decorator

