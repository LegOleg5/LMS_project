from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ProfileForm(FlaskForm):
    enter_code = StringField('Учительский код:', validators=[DataRequired()])
    submit = SubmitField('Войти в группу')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    is_teacher = BooleanField('Я учитель')
    submit = SubmitField('Зарегестрироваться')


class LessonCreationForm(FlaskForm):
    title = StringField('Тема урока:', validators=[DataRequired()])
    theory = TextAreaField('Теоретический материал:')
    submit = SubmitField('Создать урок')


class StudyForm(FlaskForm):
    submit = SubmitField('Создать')