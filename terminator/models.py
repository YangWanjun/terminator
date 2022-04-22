from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from terminator.database import db


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(TimestampMixin, db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email


class Service(TimestampMixin, db.Model):
    __tablename__ = 't_service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    upgrade_file = db.Column(db.String(200), nullable=False)


class MaintenanceInfo(TimestampMixin, db.Model):
    __tablename__ = 't_maintenance_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, ForeignKey('t_service.id'), nullable=False)
    service = relationship("Service", backref=db.backref('maintenance_info_set', lazy=True))
    start_dt = db.Column(db.DateTime, nullable=False)
    end_dt = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(2000), nullable=True)

    @property
    def status(self):
        if self.start_dt > datetime.now():
            return '01'
        elif self.start_dt <= datetime.now() <= self.end_dt:
            return '10'
        else:
            return '90'
