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
    working_day = db.Column(db.Numeric, nullable=False)  # Добавленный столбец
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

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
    profiles_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False) 

    profiles = db.relationship('Profile', backref=db.backref('overtime_reports', lazy=True))  

    def __repr__(self):
        return f'<OvertimeReport {self.id}, {self.project_name}>'

    



class ProjectAccounting(db.Model):
    __tablename__ = 'project_accounting'  # Имя таблицы в базе данных

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text, nullable=False)
    num = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<ProjectAccounting {self.project_name}>'
    

    from app import db  # Убедитесь, что вы импортировали экземпляр SQLAlchemy как db




class ProjectReports(db.Model):
    __tablename__ = 'project_reports'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_accounting.id'), nullable=False)
    profiles_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    location_work = db.Column(db.String(255), nullable=False)
    hours_spent = db.Column(db.Numeric(5, 1), nullable=False)
    works = db.Column(db.Text)
    clarification = db.Column(db.Text)

    # Отношения к другим моделям
    profile = db.relationship('Profile', backref=db.backref('project_reports', lazy=True))
    project = db.relationship('ProjectAccounting', backref=db.backref('project_reports', lazy=True))

    def __repr__(self):
        return f'<ProjectReports {self.id}, {self.report_date}>'








# class WorkReport(db.Model):
#     __tablename__ = 'work_report'

#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('project_accounting.id'), nullable=False)
#     profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)  # Изменено здесь
#     project_date = db.Column(db.Date, nullable=False)
#     task_performed = db.Column(db.Text, nullable=False)
#     hours_spent = db.Column(db.Numeric, nullable=False)

#     profile = db.relationship('Profile', backref=db.backref('work_reports', lazy=True))  # Изменено здесь
#     project = db.relationship('ProjectAccounting', backref=db.backref('work_reports', lazy=True))

#     def __repr__(self):
#         return f'<WorkReport {self.task_performed}>'

