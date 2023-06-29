from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constant import ID_NOT_FOUND, JSON_IS_EMPTY, JSON_NOT_FULL
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    try:
        data = request.get_json()
    except Exception:
        raise InvalidAPIUsage(JSON_IS_EMPTY)
    if not data:
        raise InvalidAPIUsage(JSON_IS_EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(JSON_NOT_FULL)
    url_map = URLMap.short_api_handler(data)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short>/', methods=['GET'])
def get_url_map(short):
    url_map = URLMap.get_by_short(short)
    if not url_map:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
