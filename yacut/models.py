import random
import re
from datetime import datetime
from re import escape

from flask import url_for

from yacut import db
from .constant import (
    SHORT_AUTO_LENGTH, SHORT_GENERATE_COUNT, SHORT_MAX_LENGTH, SYMBOLS_IN_SHORT,
    URL_ORIGINAL_MAX_LENGTH)
from .error_handlers import (
    Original_exist_error, Short_exist_error, Short_generate_error,
    Short_max_length_error)


SHORT_REGEX = re.compile(rf'^[{escape(SYMBOLS_IN_SHORT)}]*$')
LONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
EXIST = 'Имя {name} уже занято!'
REDIRECT_VIEW = 'redirect_view'
INDEX_API_VIEW = 'create_url_map'
SHORT_GENERATE_ERROR = (
    'При всех попытках генерации короткой ссылки '
    'получено значение, которое имеется в базе.')


def get_unique_short():
    for _ in range(SHORT_GENERATE_COUNT):
        short = ''.join(
            random.sample(SYMBOLS_IN_SHORT, SHORT_AUTO_LENGTH)
        )
        if not URLMap.get(short=short):
            return short
        raise Short_generate_error(SHORT_GENERATE_ERROR)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_ORIGINAL_MAX_LENGTH), unique=True)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(REDIRECT_VIEW, short=self.short, _external=True)
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short, view_name):
        if not short:
            short = get_unique_short()
        elif view_name == INDEX_API_VIEW and len(short) > SHORT_MAX_LENGTH:
            raise Short_max_length_error(LONG_SHORT)
        elif not re.search(SHORT_REGEX, short):
            raise ValueError(LONG_SHORT)
        elif view_name == INDEX_API_VIEW and URLMap.query.filter_by(original=original).first():
            raise Original_exist_error(EXIST.format(name=short))
        elif URLMap.get(short):
            raise Short_exist_error(EXIST.format(name=short))
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
