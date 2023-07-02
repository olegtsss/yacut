import random
import re
from datetime import datetime
from re import escape
import validators

from flask import url_for

from yacut import db
from .constant import (
    SHORT_AUTO_LENGTH, SHORT_GENERATE_COUNT, SHORT_MAX_LENGTH, SYMBOLS_IN_SHORT,
    URL_ORIGINAL_MAX_LENGTH)
from .error_handlers import (
    ShortExistError, ShortGenerateError, ShortMaxLengthError)


SHORT_REGEX = re.compile(rf'^[{escape(SYMBOLS_IN_SHORT)}]*$')
LONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
ORIGINAL_LENGTH_ERROR = (
    'Указано не коректное значение для url. '
    f'Максимальная длина {URL_ORIGINAL_MAX_LENGTH}, '
    'получено значение {real_length}')
ORIGINAL_ERROR = 'Указанное значение {original} не похоже на url'
EXIST = 'Имя {name} уже занято!'
REDIRECT_VIEW = 'redirect_view'
SHORT_GENERATE_ERROR = (
    f'При {SHORT_GENERATE_COUNT} попытках генерации короткой ссылки '
    'получено значение, которое имеется в базе.')


def get_unique_short():
    for _ in range(SHORT_GENERATE_COUNT):
        short = ''.join(
            random.sample(SYMBOLS_IN_SHORT, SHORT_AUTO_LENGTH)
        )
        if not URLMap.get(short=short):
            return short
        raise ShortGenerateError(SHORT_GENERATE_ERROR)


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
    def create(original, short, need_validation=False):
        if not short:
            short = get_unique_short()
        elif need_validation:
            if len(short) > SHORT_MAX_LENGTH:
                raise ShortMaxLengthError(LONG_SHORT)
            if not re.search(SHORT_REGEX, short):
                raise ValueError(LONG_SHORT)
            if URLMap.get(short):
                raise ShortExistError(EXIST.format(name=short))
        if len(original) > URL_ORIGINAL_MAX_LENGTH:
            raise ValueError(
                ORIGINAL_LENGTH_ERROR.format(real_length=len(original)))
        if not validators.url(original):
            raise ValueError(ORIGINAL_ERROR.format(original=original))
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
