import os
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
    'user': 'root',
    'password': os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD'],
    'host': os.environ['MYSQL_PORT_3306_TCP_ADDR'],
    'db': 'maintenance_info'
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
