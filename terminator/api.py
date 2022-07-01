import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import and_

from terminator.models import Service, MaintenanceInfo
from terminator.utils.signature import validate_token

router = Blueprint('api', __name__, url_prefix='/api')


@router.route('/maintenances', methods=('GET',))
def maintenance_list():
    header_signature = request.headers.get('X-Signature', None)
    domain = request.args.get('service')
    service = Service.query.filter_by(domain=domain).first()
    now = datetime.datetime.now()
    if validate_token(header_signature, service.secret_key):
        qs_maintenance = MaintenanceInfo.query.filter(and_(
            MaintenanceInfo.end_dt >= now.strftime('%Y-%m-%d %H:%M:%S'),
            MaintenanceInfo.service == service,
        )).order_by('start_dt')
        results = [{
            'start_dt': m.start_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'end_dt': m.end_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'content': m.content,
        } for m in qs_maintenance]
        return jsonify(results)
    else:
        return jsonify({'valid': False}), 401
