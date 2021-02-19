import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# from flaskr.db import get_db

bp = Blueprint('sqli1', __name__, url_prefix='/vulnerabilities')

@bp.route('/login', methods='POST')
def login():
    return request.form['username']
    if valid_login(request.form['username'], request.form['password']):
        return log_the_user_in(request.form['username'])
    else:
        error = 'Invalid username/password'
