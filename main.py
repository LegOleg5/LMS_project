from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from TCG import generate_code
from data import db_session
from data.data_types import User, Lesson, Task
from forms.forms import LoginForm, RegisterForm, ProfileForm, LessonCreationForm, StudyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def index():
    return render_template("base.html", title='Регистрация')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            is_teacher=form.is_teacher.data
        )
        if form.is_teacher.data:
            code = generate_code()
            while True:
                for user in db_sess.query(User).all():
                    if user.teacher_code == code:
                        break
                else:
                    break
                code = generate_code()

            user.set_code(code)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.teacher_code == form.enter_code.data).all():
            user.teacher_code = form.enter_code.data
            db_sess.commit()
        else:
            return render_template('profile.html', title='Профиль', user=user, message='Учителя с таким кодом не существует', form=form)
        return render_template('profile.html', title='Профиль', user=user, form=form)
    return render_template('profile.html', title='Профиль', user=user, form=form)


@app.route('/study/lesson_creation', methods=['GET', 'POST'])
def lesson_creation():
    form = LessonCreationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        lesson = Lesson(
            title=form.title.data,
            theory=form.theory.data,
            teacher_code=user.teacher_code
        )
        db_sess.add(lesson)
        db_sess.commit()
        return redirect('/study')
    return render_template('lesson_creation.html', title='Создание урока', form=form)


@app.route('/study', methods=['GET', 'POST'])
def study():
    form = StudyForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    lessons = db_sess.query(Lesson).filter(Lesson.teacher_code == user.teacher_code).all()
    if form.validate_on_submit():
        return redirect('/study/lesson_creation')
    return render_template('study.html', title='Обучение',  lessons=lessons, user=user, form=form)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1', debug=True)
