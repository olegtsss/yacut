import random
import string

from yacut import URL_SHORT_AUTO_LENGTH

from .models import URLMap


def get_unique_short_id():
    short_id = ''.join(
        random.choice(string.ascii_letters + string.digits)
        for symbol in range(URL_SHORT_AUTO_LENGTH)
    )
    if URLMap.query.filter_by(short=short_id).first():
        short_id = get_unique_short_id()
    return short_id


def validate_short(short):
    for symbol in short:
        if symbol not in (string.ascii_letters + string.digits):
            return False
    return True
