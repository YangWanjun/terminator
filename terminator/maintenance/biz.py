import os
from datetime import datetime
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

from terminator.models import MaintenanceInfo, Service


def start_maintenance(upgrade_file_path: Path):
    """メンテナンス開始"""
    if not upgrade_file_path.exists():
        f = open(upgrade_file_path, 'w')
        f.close()


def end_maintenance(upgrade_file_path: Path):
    if upgrade_file_path.exists():
        os.remove(upgrade_file_path)


def add_schedule(maintenance: MaintenanceInfo):
    service = Service.query.filter_by(id=maintenance.service_id).first()
    upgrade_file_path = Path(service.upgrade_file)
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=start_maintenance, id=f'{maintenance.id}_start',
        trigger='date', run_date=maintenance.start_dt, args=(upgrade_file_path,)
    )
    scheduler.add_job(
        func=end_maintenance, id=f'{maintenance.id}_end',
        trigger='date', run_date=maintenance.end_dt, args=(upgrade_file_path,)
    )
    scheduler.start()


def reload_schedule(app):
    with app.app_context():
        now = datetime.now()
        qs_maintenance = MaintenanceInfo.query.filter(
            MaintenanceInfo.end_dt >= now
        )
        scheduler = BackgroundScheduler()
        for maintenance in qs_maintenance:
            upgrade_file_path = Path(maintenance.service.upgrade_file)
            start_dt = max((maintenance.start_dt, now))
            scheduler.add_job(
                func=start_maintenance, id=f'{maintenance.id}_start',
                trigger='date', run_date=start_dt, args=(upgrade_file_path,)
            )
            scheduler.add_job(
                func=end_maintenance, id=f'{maintenance.id}_end',
                trigger='date', run_date=maintenance.end_dt, args=(upgrade_file_path,)
            )
        scheduler.start()
