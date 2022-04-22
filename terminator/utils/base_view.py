import typing as t

from flask import render_template, g, redirect, url_for
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from terminator.database import db
from terminator.hooks import transaction


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

    def get_object(self, **kwargs):
        return self.model.query.filter_by(id=kwargs.get('pk')).first_or_404()

    @transaction
    def dispatch_request(self, *args: t.Any, **kwargs: t.Any) -> ResponseReturnValue:
        return super(BaseDeleteView, self).dispatch_request(*args, **kwargs)

    def post_extra(self, obj, **kwargs):
        pass

    def post(self, *args, **kwargs):
        obj = self.get_object(**kwargs)
        self.post_extra(obj, **kwargs)
        db.session.delete(obj)
        return {}


class BaseMethodView(MethodView):
    decorators = [login_required]
    template_name = None

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    @transaction
    def dispatch_request(self, *args: t.Any, **kwargs: t.Any) -> ResponseReturnValue:
        return super(BaseMethodView, self).dispatch_request(*args, **kwargs)

    def get(self, *args, **kwargs):
        context = {**self.get_context_data(*args, **kwargs)}
        return self.render_template(context)

    def get_context_data(self, *args, **kwargs):
        raise NotImplementedError
