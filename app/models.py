from app import db
from datetime import datetime
from flask_login import UserMixin  # Убедитесь, что Flask-Login установлен

class Role(db.Model):
    __tablename__ = 'roles'  # Явно указываем имя таблицы
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)  # Указываем ограничение длины
    label = db.Column(db.String(50), nullable=False)  # Аналогично

    def __repr__(self):
        return f'<Role {self.id}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Явно указываем имя таблицы
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Ссылка на имя таблицы

    # Связь с моделью Role
    role = db.relationship('Role', backref='users', lazy=True)

    def __repr__(self):
        return f"<User {self.id}>"

    # Функции проверки роли пользователя
    def is_admin(self):
        return self.role and self.role.code == 'admin'

    def is_manager(self):
        return self.role and self.role.code == 'manager'

    def is_employee(self):
        return self.role and self.role.code == 'employee'
