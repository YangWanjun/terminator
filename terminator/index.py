from urllib.parse import urlparse

from flask import Blueprint, request, render_template, current_app

from terminator.models import Service, MaintenanceInfo

router = Blueprint('index', __name__, url_prefix='/')


@router.route('/', methods=('GET',))
def index():
    current_app.logger.info('origin:%s, referrer: %s', request.origin, request.referrer)
    domain = request.args.get('service')
    service = Service.query.filter_by(domain=domain).first_or_404()
    if service.is_separate and urlparse(request.referrer).netloc == domain:
        return {}, 503
    start_dt = end_dt = None
    content = f'現在 {domain or "システム"} はメンテナンス中です、しばらくお待ちください。'
    if domain:
        maintenance_info = MaintenanceInfo.query.filter(MaintenanceInfo.service.has(domain=domain)).first()
        if maintenance_info:
            content = maintenance_info.content
            start_dt = maintenance_info.start_dt
            end_dt = maintenance_info.end_dt
    return render_template('index.html', start_dt=start_dt, end_dt=end_dt, content=content)
