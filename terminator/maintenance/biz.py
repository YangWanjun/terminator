import datetime
import os
from pathlib import Path

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

from terminator.database import db
from terminator.models import MaintenanceInfo, Service

scheduler: BackgroundScheduler = None


def start_maintenance(upgrade_file_path: Path):
    """メンテナンス開始"""
    if not upgrade_file_path.exists():
        os.makedirs(upgrade_file_path.parent, exist_ok=True)
        f = open(upgrade_file_path, 'w')
        f.close()


def end_maintenance(upgrade_file_path: Path):
    if upgrade_file_path.exists():
        try:
            os.remove(upgrade_file_path)
        except OSError:
            pass


def add_schedule(maintenance: MaintenanceInfo):
    service = Service.query.filter_by(id=maintenance.service_id).first()
    upgrade_file_path = Path(service.upgrade_file)
    start_job_id, end_job_id = maintenance.get_jobs_id()
    scheduler.add_job(
        func=start_maintenance, id=start_job_id, replace_existing=True,
        trigger='date', run_date=maintenance.start_dt, args=(upgrade_file_path,)
    )
    scheduler.add_job(
        func=end_maintenance, id=end_job_id, replace_existing=True,
        trigger='date', run_date=maintenance.end_dt, args=(upgrade_file_path,)
    )


def remove_schedule(maintenance: MaintenanceInfo):
    start_job_id, end_job_id = maintenance.get_jobs_id()
    if scheduler.get_job(start_job_id, jobstore='default'):
        scheduler.remove_job(start_job_id, jobstore='default')
    if scheduler.get_job(end_job_id, jobstore='default'):
        scheduler.remove_job(end_job_id, jobstore='default')


def reload_schedule(app):
    with app.app_context():
        job_stores = {
            'default': SQLAlchemyJobStore(engine=db.engine, tablename='t_job')
        }
        job_defaults = {
            'replace_existing': True
        }
        global scheduler
        scheduler = BackgroundScheduler(
            jobstores=job_stores,
            job_defaults=job_defaults,
            timezone=timezone('Asia/Tokyo'),
        )
        scheduler.start()
