from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut import URL_ORIGINAL_MAX_LENGTH, URL_SHORT_MAX_LENGTH


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, URL_ORIGINAL_MAX_LENGTH)
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, URL_SHORT_MAX_LENGTH),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
