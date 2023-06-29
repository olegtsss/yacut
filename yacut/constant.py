import re
import string


URL_ORIGINAL_MAX_LENGTH = 2048
URL_SHORT_MAX_LENGTH = 16
URL_SHORT_AUTO_LENGTH = 6
SYMBOLS_IN_SHORT = string.ascii_letters + string.digits

INDEX_VIEW = 'index_view'
REDIRECT_VIEW = 'redirect_view'

LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'
CUSTOM_SHORT_LINK = 'Ваш вариант короткой ссылки'
CREATE_BUTTON = 'Создать'

CATEGORY_INFO = 'info'
CATEGORY_HREF = 'href'
HREF_CREATE = 'Ваша новая ссылка готова:'

JSON_NOT_FULL = '"url" является обязательным полем!'
JSON_IS_EMPTY = 'Отсутствует тело запроса'
ID_NOT_FOUND = 'Указанный id не найден'

EXIST = 'Имя {name} уже занято!'
EXIST_API = 'Имя "{name}" уже занято.'
LONG_SHORT = 'Указано недопустимое имя для короткой ссылки'

SHORT_GENERATE_COUNT = 10
SHORT_GENERATE_ERROR = (
    'При генерации короткой ссылки получено значение, которое имеется в базе. '
    'Количество попыток: {count}')
SHORT_REGEX = re.compile(r"^[a-zA-Z0-9]*$")
