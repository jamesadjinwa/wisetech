from datetime import datetime
from flask import render_template, current_app, jsonify, redirect, \
    url_for, flash, g, request
from flask_login import current_user, login_required
from app.main.forms import EditUserProfileForm, CreateTicketForm
from flask_babel import _, get_locale
from app import db
from app.models import User
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # form = CreateTicketForm()
    # if forms.validate_on_submit():
    #     ticket = CreateTicketForm(
    #         id_client=form.clientname.data,
    #         id_equipment=form.equip_type.data,

    #     )

    user = {'username': current_user.username}
    return render_template('index.html', title='Home', user=user)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    #posts = user.posts.order_by(Post.timestamp.desc()).paginate(
    #    page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('main.user', username=user.username,
    #                    page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('main.user', username=user.username,
    #                    page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user)

@bp.route('/edit_user_profile', methods=['GET', 'POST'])
@login_required
def edit_user_profile():
    form = EditUserProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_user_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_user_profile.html', title=_('Edit User Profile'),
                           form=form)

