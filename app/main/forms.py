from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User, Group, Profil, Client, Service, Equipment, Ticket


class EditUserProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class CreateTicketForm(FlaskForm):
    clientname = StringField(_l('Customer'), validators=[DataRequired()])
    equip_type = StringField(_l('Equipement type'), validators=[DataRequired()])
    brand = StringField(_l('Brand'), validators=[DataRequired()])
    model = StringField(_l('Model'), validators=[DataRequired()])
    serial = StringField(_l('Model'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class EditTicketForm(FlaskForm):
    pass


class CreateProfileForm(FlaskForm):
    pass


class EditProfileForm(FlaskForm):
    pass


class CreateGroupForm(FlaskForm):
    pass


class EditGroupForm(FlaskForm):
    pass


