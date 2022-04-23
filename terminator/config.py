import os
from datetime import timedelta
from urllib.parse import quote

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
    'user': os.environ['MYSQL_ENV_MYSQL_USER'],
    'password': quote(os.environ['MYSQL_ENV_MYSQL_ROOT_PASSWORD']),
    'host': quote(os.environ['MYSQL_PORT_3306_TCP_ADDR']),
    'db': 'maintenance'
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
# Custom config
CAS_VALIDATE_URL = 'https://cas.e-business.co.jp/p3/serviceValidate'
