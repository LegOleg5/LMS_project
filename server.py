from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from TCG import generate_code
from data import db_session
from data.data_types import User, Lesson, Task, Solution
from forms.forms import LoginForm, RegisterForm, ProfileForm, LessonCreationForm, StudyForm, LessonForm, TaskCreationForm, TaskForm

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
            return render_template('profile.html', title='Профиль', user=user,
                                   message='Учителя с таким кодом не существует', form=form)
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


@app.route('/study/lesson', methods=['GET', 'POST'])
def lesson():
    form = LessonForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    lesson = db_sess.query(Lesson).filter(Lesson.id == request.args.get('id')).first()
    tasks = db_sess.query(Task).filter(Task.lesson_id == lesson.id).all()
    if form.validate_on_submit():
        pass
    return render_template('lesson.html', title=f'{lesson.title}', lesson=lesson, user=user, tasks=tasks, form=form)


@app.route('/study/lesson/task_creation', methods=['GET', 'POST'])
def task_creation():
    form = TaskCreationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        lesson = db_sess.query(Lesson).filter(Lesson.id == request.args.get('id')).first()
        task = Task(
            title=form.title.data,
            cond=form.cond.data,
            lesson_id=lesson.id
        )
        db_sess.add(task)
        db_sess.commit()
        return redirect(f'/study/lesson?id={lesson.id}')
    return render_template('task_creation.html', title='Создание урока', form=form)


@app.route('/study/lesson/task', methods=['GET', 'POST'])
def task():
    form = TaskForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    task = db_sess.query(Task).filter(Task.id == request.args.get('id')).first()
    lesson = db_sess.query(Lesson).filter(Lesson.id == task.lesson_id).first()
    solutions = db_sess.query(Solution).filter(Solution.task_id == task.id, Solution.checked == None).all()
    user_solution = db_sess.query(Solution).filter(Solution.task_id == task.id, Solution.user_id == user.id).first()
    if form.validate_on_submit():
        if db_sess.query(Solution).filter(Solution.task_id == task.id, Solution.user_id == user.id).first():
            solution = db_sess.query(Solution).filter(Solution.task_id == task.id, Solution.user_id == user.id).first()
            solution.text = form.solution.data
            db_sess.commit()
        else:
            solution = Solution(
                text=form.solution.data,
                user_id=user.id,
                task_id=task.id
            )
            db_sess.add(solution)
            db_sess.commit()

        return render_template('task.html', title=task.title, task=task, solutions=solutions,
                               user_solution=user_solution, user=user, form=form)
    return render_template('task.html', title=task.title, task=task, solutions=solutions,
                           user_solution=user_solution, user=user, form=form)


@app.route('/study/lesson/task/check/<solution_id>/<verdict>', methods=['GET', 'POST'])
def check(solution_id, verdict):
    db_sess = db_session.create_session()
    solution = db_sess.query(Solution).filter(Solution.id == int(str(solution_id).replace('!1=', ''))).first()
    if int(str(verdict).replace('!2=', '')) == 1:
        solution.correct = True
    else:
        solution.correct = False
    solution.checked = True
    db_sess.commit()
    return redirect(f'/study/lesson/task?id={solution.task_id}')



if __name__ == '__server__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1', debug=True)
