from app import db
from datetime import datetime
from flask_login import UserMixin  # Убедитесь, что Flask-Login установлен



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Role {self.id}>'
    
class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Опционально: добавьте связь с таблицей пользователей, если нужно
    user = db.relationship('User', backref=db.backref('profiles', lazy=True))

    def __repr__(self):
        return f'<Profile {self.name}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User {self.id}>"

    # Функции проверки роли пользователя
    def is_admin(self):
        return self.role and self.role.code == 'admin'

    def is_manager(self):
        return self.role and self.role.code == 'manager'

    def is_employee(self):
        return self.role and self.role.code == 'employee'


class OvertimeReport(db.Model):
    __tablename__ = 'overtime_report'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    task_date = db.Column(db.Date, nullable=False)
    day_type = db.Column(db.String(50), nullable=False)
    hours_worked = db.Column(db.Numeric(5, 1), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('overtime_report', lazy=True))

    def __repr__(self):
        return f'<OvertimeReport {self.id}, {self.project_name}>'