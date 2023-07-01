from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import (
    InvalidAPIUsage, Original_exist_error, Short_exist_error,
    Short_generate_error)
from .models import INDEX_API_VIEW, URLMap


ID_NOT_FOUND = 'Указанный id не найден'
JSON_IS_EMPTY = 'Отсутствует тело запроса'
JSON_NOT_FULL = '"url" является обязательным полем!'
EXIST_API = 'Имя "{name}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    if request.data == b'':
        raise InvalidAPIUsage(JSON_IS_EMPTY)
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(JSON_IS_EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(JSON_NOT_FULL)
    try:
        short = data.get('custom_id')
        return jsonify(
            URLMap.create(
                original=data['url'],
                short=short,
                view_name=INDEX_API_VIEW).to_dict(),
        ), HTTPStatus.CREATED
    except (Original_exist_error, Short_exist_error):
        raise InvalidAPIUsage(EXIST_API.format(name=short))
    except Short_generate_error as error:
        raise InvalidAPIUsage(str(error))
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<short>/', methods=['GET'])
def get_url_map(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
