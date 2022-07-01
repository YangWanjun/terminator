import datetime
import hmac
from hashlib import sha256


def validate_token(header_signature: str, token: str) -> bool:
    encoding = 'utf-8'
    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha256':
        return False
    today = datetime.date.today()
    mac = hmac.new(token.encode(encoding), msg=today.strftime('%Y%m%d').encode(encoding), digestmod=sha256)
    print(mac.hexdigest())
    if not hmac.compare_digest(mac.hexdigest().encode(encoding), signature.encode(encoding)):
        return False
    return True
