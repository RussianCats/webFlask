import datetime
from sqlalchemy.orm import joinedload
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config


# конфигурация

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# После инициализации db
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Настройка функции загрузчика пользователя
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))




class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<roles {self.id}>'

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f"<users {self.id}>"
    
    # Добавьте связь с моделью Roles
    role = db.relationship('Roles')
    # Добавьте связь с моделью Profiles
    profiles = db.relationship('Profiles', backref='user', uselist=False)


    def is_admin(self):
        return self.role and self.role.code == 'admin'

    def is_manager(self):
        return self.role and self.role.code == 'manager'

    def is_employee(self):
        return self.role and self.role.code == 'employee'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return f"<profiles {self.id}>"
    
@app.route("/index")
@app.route("/")
def index():
    if current_user.is_authenticated:
        # Логика для авторизованных пользователей
        return render_template('index.html', is_authenticated=True)
    else:
        # Логика для неавторизованных пользователей
        return render_template('index.html', is_authenticated=False)

@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            # заносим данные пользователя в бд с кешом пароля
            hash = generate_password_hash(request.form['psw'])
            u = Users(login=request.form['login'], psw=hash, roles_id=request.form['role'])
            db.session.add(u)
            db.session.flush()
            # добавляем данные в профайлес
            p = Profiles(name=request.form['name'], user_id = u.id)
            db.session.add(p)
            db.session.commit() 
            print(f"Пользователь зарегестрирован {request.form['login']}")
        except Exception as e:
            # если ошибки, то откатываем состояние
            db.session.rollback()
            print(f"Ошибка записи пользователя в БД: {e}")

    return render_template("register.html", title="Регистрация")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['psw']
        user = Users.query.filter_by(login=login).first()
        if user and check_password_hash(user.psw, password):
            print("Пользователь авторизован")
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin_area', methods=("POST", "GET"))
@login_required
def admin_area():
    if not current_user.is_admin():
        flash('Доступ разрешен только администраторам!')
        return redirect(url_for('index'))
    
    if request.method == "POST":
        login = request.form['login']
        password = request.form['psw']
        name = request.form['name']
        role_id = request.form['role']

        # Здесь должна быть проверка корректности введенных данных
        # Например, проверить, не существует ли уже пользователя с таким логином

        try:
            # Заносим данные пользователя в БД с хешированным паролем
            hashed_password = generate_password_hash(password)
            new_user = Users(login=login, psw=hashed_password, roles_id=role_id)

            db.session.add(new_user)
            db.session.flush()  # Это позволяет получить ID для нового пользователя

            # Добавляем данные в профили
            new_profile = Profiles(name=name, user_id=new_user.id)
            db.session.add(new_profile)
            db.session.commit()

            flash(f"Пользователь {login} успешно зарегистрирован")
        except Exception as e:
            # Если возникают ошибки, то откатываем состояние
            db.session.rollback()
            flash(f"Ошибка записи пользователя в БД: {e}")

    users = Users.query.options(joinedload(Users.role), joinedload(Users.profiles)).all()
    return render_template('admin_area.html', users=users)

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    if not current_user.is_admin():
        flash('Доступ разрешен только администраторам!')
        return redirect(url_for('index'))

    user_id = request.form.get('userId')
    user = Users.query.get(user_id)

    if user:
        try:
            # Удаляем связанный профиль, если он существует
            if user.profiles:
                db.session.delete(user.profiles)

            # Удаляем пользователя
            db.session.delete(user)
            db.session.commit()
            flash('Пользователь успешно удален')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при удалении пользователя: {e}')
    else:
        flash('Пользователь не найден')

    return redirect(url_for('admin_area'))

if __name__ == "__main__":
    app.run(debug=True)
