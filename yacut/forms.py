from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .constant import (CREATE_BUTTON, CUSTOM_SHORT_LINK, EXIST, LONG_LINK,
                       LONG_SHORT, REQUIRED_FIELD, SHORT_REGEX,
                       URL_ORIGINAL_MAX_LENGTH, URL_SHORT_MAX_LENGTH)
from .models import URLMap


class UrlForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=URL_ORIGINAL_MAX_LENGTH)
        ]
    )
    custom_id = URLField(
        CUSTOM_SHORT_LINK,
        validators=[
            Length(max=URL_SHORT_MAX_LENGTH),
            Optional(),
            Regexp(SHORT_REGEX, message=LONG_SHORT)
        ]
    )
    submit = SubmitField(CREATE_BUTTON)

    def validate_custom_id(self, custom_id):
        if custom_id.data and URLMap.get_by_short(short=custom_id.data):
            raise ValidationError(EXIST.format(name=custom_id.data))
