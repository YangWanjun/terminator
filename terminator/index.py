import datetime

from flask import Blueprint, request, render_template
from flask_cors import cross_origin
from sqlalchemy import and_

from terminator.models import MaintenanceInfo

router = Blueprint('index', __name__, url_prefix='/')


@router.route('/', methods=('GET',))
@cross_origin()
def index():
    request_format = request.args.get('format')
    if request_format == 'json':
        return {}, 503
    start_dt = end_dt = None
    domain = request.args.get('service')
    content = f'現在 {domain or "システム"} はメンテナンス中です、しばらくお待ちください。'
    if domain:
        now = datetime.datetime.utcnow()
        maintenance_info = MaintenanceInfo.query.filter(and_(
            MaintenanceInfo.start_dt <= now.strftime('%Y-%m-%d %H:%M:%S'),
            MaintenanceInfo.end_dt >= now.strftime('%Y-%m-%d %H:%M:%S'),
            MaintenanceInfo.service.has(domain=domain),
        )).first()
        if maintenance_info:
            content = maintenance_info.content
            start_dt = maintenance_info.start_dt
            end_dt = maintenance_info.end_dt
    return render_template('index.html', start_dt=start_dt, end_dt=end_dt, content=content)
