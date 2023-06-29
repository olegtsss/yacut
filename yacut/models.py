import random
import re
from datetime import datetime

from flask import url_for

from yacut import db
from .constant import (
    SHORT_AUTO_LENGTH, SHORT_GENERATE_COUNT, SHORT_MAX_LENGTH,
    SYMBOLS_IN_SHORT, URL_ORIGINAL_MAX_LENGTH
)


SHORT_REGEX = re.compile(rf'^[{SYMBOLS_IN_SHORT}]*$')
LONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
EXIST = 'Имя {name} уже занято!'
REDIRECT_VIEW = 'redirect_view'
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
    raise UserWarning(SHORT_GENERATE_ERROR)


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
    def create(original, short):
        url = URLMap(original=original, short=short)
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def handler(original, short):
        if URLMap.query.filter_by(original=original).first():
            raise NameError(EXIST.format(name=short))
        if not short:
            short = get_unique_short()
        elif (
            len(short) > SHORT_MAX_LENGTH or
            not re.search(SHORT_REGEX, short)
        ):
            raise ValueError(LONG_SHORT)
        return URLMap.create(original=original, short=short)
