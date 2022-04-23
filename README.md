## Init database

```shell
# Windows command
SET "FLASK_APP=terminator/__init__.py" && SET "MYSQL_ENV_MYSQL_USER=root" && SET "MYSQL_ENV_MYSQL_ROOT_PASSWORD=root" && SET "MYSQL_PORT_3306_TCP_ADDR=127.0.0.1" && flask drop-tables
SET "FLASK_APP=terminator/__init__.py" && SET "MYSQL_ENV_MYSQL_USER=root" && SET "MYSQL_ENV_MYSQL_ROOT_PASSWORD=root" && SET "MYSQL_PORT_3306_TCP_ADDR=127.0.0.1" && flask init-db
```

## Create user
```shell
# Windows command
SET "FLASK_APP=terminator/__init__.py" && SET "MYSQL_ENV_MYSQL_USER=root" && SET "MYSQL_ENV_MYSQL_ROOT_PASSWORD=root" && SET "MYSQL_PORT_3306_TCP_ADDR=127.0.0.1" && flask create-user
```
