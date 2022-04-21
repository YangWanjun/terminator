## Init database

```shell
# Windows command
SET "FLASK_APP=terminator/__init__.py" && flask drop-tables
SET "FLASK_APP=terminator/__init__.py" && flask init-db
```

## Create user
```shell
# Windows command
SET "FLASK_APP=terminator/__init__.py" && flask create-user
```
