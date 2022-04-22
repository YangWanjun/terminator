import os
from pathlib import Path

from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from terminator.database import db
from terminator.models import MaintenanceInfo, Service

scheduler: BackgroundScheduler = None


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
    scheduler.add_job(
        func=start_maintenance, id=f'{maintenance.id}_start',
        trigger='date', run_date=maintenance.start_dt, args=(upgrade_file_path,)
    )
    scheduler.add_job(
        func=end_maintenance, id=f'{maintenance.id}_end',
        trigger='date', run_date=maintenance.end_dt, args=(upgrade_file_path,)
    )


def remove_schedule(maintenance: MaintenanceInfo):
    try:
        scheduler.remove_job(f'{maintenance.id}_start', jobstore='default')
    except JobLookupError:
        pass
    try:
        scheduler.remove_job(f'{maintenance.id}_end', jobstore='default')
    except JobLookupError:
        pass


def reload_schedule(app):
    with app.app_context():
        job_stores = {
            'default': SQLAlchemyJobStore(engine=db.engine, tablename='t_job')
        }
        global scheduler
        scheduler = BackgroundScheduler(jobstores=job_stores)
        scheduler.start()
