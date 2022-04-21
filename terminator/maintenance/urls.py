from flask import Flask

from terminator.maintenance.views import MaintenanceListView, MaintenanceDetailView, MaintenanceDeleteView, \
    ServiceListView, ServiceDetailView, ServiceDeleteView


def register_url(app: Flask):
    list_view = MaintenanceListView.as_view('maintenance-list')
    add_view = MaintenanceDetailView.as_view('maintenance-add')
    change_view = MaintenanceDetailView.as_view('maintenance-change')
    delete_view = MaintenanceDeleteView.as_view('maintenance-delete')
    app.add_url_rule('/maintenance', view_func=list_view, methods=('GET',))
    app.add_url_rule('/maintenance/add', view_func=add_view, methods=('GET', 'POST'))
    app.add_url_rule('/maintenance/<int:pk>', view_func=change_view, methods=('GET', 'POST'))
    app.add_url_rule('/maintenance/<int:pk>/delete', view_func=delete_view, methods=('POST',))

    service_list_view = ServiceListView.as_view('service-list')
    service_add_view = ServiceDetailView.as_view('service-add')
    service_change_view = ServiceDetailView.as_view('service-change')
    service_delete_view = ServiceDeleteView.as_view('service-delete')
    app.add_url_rule('/master/service', view_func=service_list_view, methods=('GET',))
    app.add_url_rule('/master/service/add', view_func=service_add_view, methods=('GET', 'POST'))
    app.add_url_rule('/master/service/<int:pk>', view_func=service_change_view, methods=('GET', 'POST'))
    app.add_url_rule('/master/service/<int:pk>/delete', view_func=service_delete_view, methods=('POST',))
