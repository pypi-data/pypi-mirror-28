# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, abort
from flask_login import login_required, login_user, logout_user
from ..forms import SigninForm
from ..models import User


# Imported
from urllib.parse import urlparse, urljoin


# bp = Blueprint('account', __name__)
#
#
# def is_safe_url(target):
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#
#     return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
#
#
# def get_redirect_target():
#     for target in request.values.get('next'), request.referrer:
#         if not target:
#             continue
#         if is_safe_url(target):
#             return target
#
#
# def redirect_back(endpoint, **values):
#     target = request.form['next']
#     if not target or not is_safe_url(target):
#         target = url_for(endpoint, **values)
#     return redirect(target)
#
#
# @bp.route('/login', methods=['GET', 'POST'])
# def signin():
#     """Sign In Login page that all are re-directed to when not logged in or session expires.
#
#     :returns html_template signin.html:
#     """
#     form = SigninForm()
#
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             form_id = request.form.get('email', None)
#
#             if form_id is None:
#                 return render_template('account/signin/signin.html', form=form)
#
#             user = User.query.filter_by(email=form_id).first()
#
#             if user is not None:
#                 if user.check_password(request.form.get('password')):
#                     login_user(user)
#                     if not is_safe_url(request.args.get('next')):
#                         return abort(400)
#                     return redirect(request.args.get('next') or url_for('site.index'))
#             else:
#                 return render_template('account/signin/signin.html', form=form)
#
#     return render_template('account/signin/signin.html', form=form)
#
#
# @bp.route("/logout", methods=["GET"])
# @login_required
# def signout():
#     """Logout the current user
#
#     :returns redirect signin.html
#     """
#     logout_user()
#     return redirect(url_for('security.signin'))
