from datetime import datetime

from flask import request

from yacut import db, URL_ORIGINAL_MAX_LENGTH, URL_SHORT_MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_ORIGINAL_MAX_LENGTH), unique=True)
    short = db.Column(db.String(URL_SHORT_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=f'{request.url_root}{self.short}'
        )
