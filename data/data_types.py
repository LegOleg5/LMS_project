import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_teacher = sqlalchemy.Column(sqlalchemy.Boolean)
    teacher_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_code(self, code):
        self.teacher_code = code

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    theory = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    teacher_code = sqlalchemy.Column(sqlalchemy.String)


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.String)
    cond = sqlalchemy.Column(sqlalchemy.Text)
    solved_by = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    def solved_by(self, user):
        self.solved_by += f'{user.id};'


class Solution(SqlAlchemyBase):
    __tablename__ = 'solutions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    text = sqlalchemy.Column(sqlalchemy.Text)
    checked = sqlalchemy.Column(sqlalchemy.Boolean)
    correct = sqlalchemy.Column(sqlalchemy.Boolean)
