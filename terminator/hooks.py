from functools import wraps

from terminator.database import db


def transaction(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if db.session.info.get('in_transaction') is True:
            return func(*args, **kwargs)
        else:
            db.session.info['in_transaction'] = True
            try:
                results = func(*args, **kwargs)
                db.session.commit()
                return results
            except Exception as ex:
                db.session.rollback()
                raise ex
            finally:
                db.session.info['in_transaction'] = False
    return decorator
