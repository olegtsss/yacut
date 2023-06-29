from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .constant import CATEGORY_HREF, CATEGORY_INFO, HREF_CREATE, REDIRECT_VIEW
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        short = URLMap.short_handler(form)
    except ValueError as error:
        flash(error, CATEGORY_INFO)
        return render_template('index.html', form=form)
    flash(HREF_CREATE, CATEGORY_INFO)
    flash(short, CATEGORY_HREF)
    return render_template(
        'index.html',
        form=form,
        short_link=url_for(REDIRECT_VIEW, short=short, _external=True)
    )


@app.route('/<short>')
def redirect_view(short):
    url_map = URLMap.get_by_short(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
