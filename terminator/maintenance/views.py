from flask import request, redirect, url_for
from sqlalchemy import desc

from terminator.database import db
from terminator.maintenance import biz
from terminator.maintenance.forms import MaintenanceInfoForm, ServiceForm
from terminator.models import MaintenanceInfo, Service
from terminator.utils import constant
from terminator.utils.base_view import BaseMethodView, BaseDeleteView


class MaintenanceListView(BaseMethodView):
    template_name = 'maintenance/maintenance_list.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'objects': MaintenanceInfo.query.order_by(desc(MaintenanceInfo.start_dt)),
        }


class MaintenanceDetailView(BaseMethodView):
    template_name = 'maintenance/maintenance_form.html'

    def get_context_data(self, *args, **kwargs):
        if 'pk' in kwargs:
            obj = MaintenanceInfo.query.filter_by(id=kwargs.get('pk')).first_or_404()
        else:
            obj = None
        form = MaintenanceInfoForm(request.form, obj=obj)
        if 'pk' in kwargs:
            form.service_id.render_kw = {'disabled': True}
            form.start_dt.render_kw = {'readonly': True}
            form.end_dt.render_kw = {'readonly': True}
        form.service_id.choices = [("", constant.EMPTY_SELECT_OPTION)] + \
                                  [(s.id, s.name) for s in Service.query.order_by('name')]
        return {
            'object': obj,
            'form': form,
        }

    def post(self, *args, **kwargs):
        context = {**self.get_context_data(*args, **kwargs)}
        form = context['form']
        if form.validate():
            if 'pk' in kwargs:
                maintenance_info = context.get('object')
                form.populate_obj(maintenance_info)
            else:
                maintenance_info = MaintenanceInfo()
                form.populate_obj(maintenance_info)
                db.session.add(maintenance_info)
                # スケジュールを立てる
                biz.add_schedule(maintenance_info)
            db.session.commit()
            return redirect(url_for('maintenance-list'))
        else:
            context['form_class'] = 'was-validated'
        return self.render_template(context)


class MaintenanceDeleteView(BaseDeleteView):
    model = MaintenanceInfo


class ServiceListView(BaseMethodView):
    template_name = 'master/service/service_list.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'objects': Service.query.order_by(desc(Service.name)),
        }


class ServiceDetailView(BaseMethodView):
    template_name = 'master/service/service_form.html'

    def get_context_data(self, *args, **kwargs):
        if 'pk' in kwargs:
            obj = Service.query.filter_by(id=kwargs.get('pk')).first_or_404()
        else:
            obj = None
        form = ServiceForm(request.form, obj=obj)
        return {
            'object': obj,
            'form': form,
        }

    def post(self, *args, **kwargs):
        context = {**self.get_context_data(*args, **kwargs)}
        form = context['form']
        if form.validate():
            if 'pk' in kwargs:
                service = context.get('object')
                form.populate_obj(service)
            else:
                service = Service()
                form.populate_obj(service)
                db.session.add(service)
            db.session.commit()
            return redirect(url_for('service-list'))
        else:
            context['form_class'] = 'was-validated'
        return self.render_template(context)


class ServiceDeleteView(BaseDeleteView):
    model = Service
