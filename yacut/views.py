from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import URL_SHORT_MAX_LENGTH

from . import app, db
from .forms import UrlForm
from .models import URLMap
from .utils import get_unique_short_id, validate_short


EXIST = 'Имя {name} уже занято!'
EXIST_API = 'Имя "{name}" уже занято.'
HREF_CREATE = 'Ваша новая ссылка готова:'
LONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
CATEGORY_INFO = 'info'
CATEGORY_HREF = 'href'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        original = form.original_link.data
        url_test = URLMap.query.filter_by(original=original).first()
        if url_test:
            flash(EXIST.format(name=url_test.short), CATEGORY_INFO)
            return render_template('main.html', form=form)
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        elif not validate_short(short) or len(short) > URL_SHORT_MAX_LENGTH:
            flash(LONG_SHORT, CATEGORY_INFO)
            return render_template('main.html', form=form)
        elif URLMap.query.filter_by(short=short).first():
            flash(EXIST.format(name=short), CATEGORY_INFO)
            return render_template('main.html', form=form)
        url = URLMap(original=original, short=short)
        db.session.add(url)
        db.session.commit()
        flash(HREF_CREATE, CATEGORY_INFO)
        flash(short, CATEGORY_HREF)
    return render_template('main.html', form=form)


@app.route('/<short>')
def opinion_view(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
