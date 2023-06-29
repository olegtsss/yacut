import random
import re
from datetime import datetime

from flask import url_for

from yacut import db

from .constant import (EXIST, EXIST_API, LONG_SHORT, REDIRECT_VIEW,
                       SHORT_GENERATE_COUNT, SHORT_GENERATE_ERROR, SHORT_REGEX,
                       SYMBOLS_IN_SHORT, URL_ORIGINAL_MAX_LENGTH,
                       URL_SHORT_AUTO_LENGTH, URL_SHORT_MAX_LENGTH)
from .error_handlers import InvalidAPIUsage


def get_unique_short_id():
    short_id = ''.join(
        random.sample(SYMBOLS_IN_SHORT, URL_SHORT_AUTO_LENGTH)
    )
    for attempt in range(SHORT_GENERATE_COUNT):
        short_id = ''.join(
            random.sample(SYMBOLS_IN_SHORT, URL_SHORT_AUTO_LENGTH)
        )
        if not URLMap.get_by_short(short=short_id):
            return short_id
    raise ValueError(SHORT_GENERATE_ERROR.format(count=SHORT_GENERATE_COUNT))


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_ORIGINAL_MAX_LENGTH), unique=True)
    short = db.Column(db.String(URL_SHORT_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(REDIRECT_VIEW, short=self.short, _external=True)
        )

    @staticmethod
    def get_by_original(original):
        return URLMap.query.filter_by(original=original).first()

    @staticmethod
    def get_by_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short):
        url = URLMap(original=original, short=short)
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def validate_symbol_in_short(short):
        if re.search(SHORT_REGEX, short):
            return True

    @staticmethod
    def validate_short(short):
        if not short:
            short = get_unique_short_id()
        elif (
            not URLMap.validate_symbol_in_short(short) or
            len(short) > URL_SHORT_MAX_LENGTH
        ):
            raise ValueError(LONG_SHORT)
        # Валидация "по базе" проходит в классе формы
        # elif URLMap.get_by_short(short=short):
        #     raise ValueError(EXIST.format(name=short))
        return short

    @staticmethod
    def validate_original(original):
        url = URLMap.get_by_original(original=original)
        if url:
            raise ValueError(EXIST.format(name=url.short))
        return original

    @staticmethod
    def short_handler(form):
        original = URLMap.validate_original(form.original_link.data)
        short = URLMap.validate_short(form.custom_id.data)
        URLMap.create(original=original, short=short)
        return short

    @staticmethod
    def short_api_handler(data):
        try:
            original = URLMap.validate_original(data['url'])
        except ValueError as error:
            raise InvalidAPIUsage(EXIST_API.format(name=str(error).split()[1]))
        try:
            short = URLMap.validate_short(data.get('custom_id'))
        except ValueError as error:
            raise InvalidAPIUsage(str(error))
        return URLMap.create(original=original, short=short)
