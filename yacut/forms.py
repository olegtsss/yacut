from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, ValidationError
)

from .constant import SHORT_MAX_LENGTH, URL_ORIGINAL_MAX_LENGTH
from .models import EXIST, LONG_SHORT, SHORT_REGEX, URLMap


LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'
CUSTOM_SHORT = 'Ваш вариант короткой ссылки'
CREATE_BUTTON = 'Создать'


class UrlForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=URL_ORIGINAL_MAX_LENGTH)
        ]
    )
    custom_id = URLField(
        CUSTOM_SHORT,
        validators=[
            Length(max=SHORT_MAX_LENGTH),
            Optional(),
            Regexp(SHORT_REGEX, message=LONG_SHORT)
        ]
    )
    submit = SubmitField(CREATE_BUTTON)

    def validate_custom_id(self, custom_id):
        if custom_id.data and URLMap.get(short=custom_id.data):
            raise ValidationError(EXIST.format(name=custom_id.data))
