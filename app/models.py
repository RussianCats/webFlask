from app import db
from datetime import datetime
from flask_login import UserMixin  # Убедитесь, что Flask-Login установлен



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Role {self.id}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    roles_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f"<User {self.id}>"

    # Функции проверки роли пользователя
    def is_admin(self):
        return self.role and self.role.code == 'admin'

    def is_manager(self):
        return self.role and self.role.code == 'manager'

    def is_employee(self):
        return self.role and self.role.code == 'employee'

class TestUser(db.Model, UserMixin):
    __tablename__ = 'test_user'  # Указываем имя таблицы

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    psw = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<TestUser {self.login}>'

