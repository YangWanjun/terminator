from flask import session, g

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
