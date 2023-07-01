from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import UrlForm
from .models import REDIRECT_VIEW, URLMap


INDEX_VIEW = 'index_view'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short=url_for(
                REDIRECT_VIEW, short=URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data,
                    view_name=INDEX_VIEW
                ).short, _external=True
            )
        )
    except ValueError as error:
        flash(error)
        return render_template(
            'index.html',
            form=form,
        )


@app.route('/<short>')
def redirect_view(short):
    url_map = URLMap.get(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
