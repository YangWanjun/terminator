from flask import render_template, g, redirect, url_for
from flask.views import MethodView

from terminator.database import db


def login_required(func):
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(url_for('account.login'))
        return func(*args, **kwargs)
    return wrapper


class BaseApiView(MethodView):
    decorators = [login_required]

    def post(self, *args, **kwargs):
        pass


class BaseDeleteView(BaseApiView):
    model = None

    def post(self, *args, **kwargs):
        obj = self.model.query.filter_by(id=kwargs.get('pk')).first_or_404()
        db.session.delete(obj)
        db.session.commit()
        return {}


class BaseMethodView(MethodView):
    decorators = [login_required]
    template_name = None

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def get(self, *args, **kwargs):
        context = {**self.get_context_data(*args, **kwargs)}
        return self.render_template(context)

    def get_context_data(self, *args, **kwargs):
        raise NotImplementedError
