from http import HTTPStatus

from flask import jsonify, request

from yacut import URL_SHORT_MAX_LENGTH

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, validate_short
from .views import EXIST_API, LONG_SHORT


JSON_NOT_FULL = '"url" является обязательным полем!'
JSON_IS_EMPTY = 'Отсутствует тело запроса'
ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(JSON_IS_EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(JSON_NOT_FULL)
    original = data['url']
    url_test = URLMap.query.filter_by(original=original).first()
    if url_test:
        raise InvalidAPIUsage(EXIST_API.format(name=url_test.short))
    short = data.get('custom_id')
    if not short:
        short = get_unique_short_id()
    elif not validate_short(short) or len(short) > URL_SHORT_MAX_LENGTH:
        raise InvalidAPIUsage(LONG_SHORT)
    elif URLMap.query.filter_by(short=short).first():
        raise InvalidAPIUsage(EXIST_API.format(name=short))
    url_map = URLMap(original=original, short=short)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short>/', methods=['GET'])
def get_url_map(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if not url_map:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
