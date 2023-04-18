from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    enter_code = StringField('Почта', validators=[DataRequired()])
    submit = SubmitField('Войти в группу')