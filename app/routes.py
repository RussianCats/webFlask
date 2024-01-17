from crypt import methods
from flask import redirect, render_template, request, flash, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, manager, db
from app.models import TestUser  
from flask_login import current_user 


@manager.user_loader
def load_user(user_id):
    return TestUser.query.get(int(user_id))


@app.route('/index')
@app.route('/')
def index():
    if current_user.is_authenticated:
        users = TestUser.query.all()  # Получаем всех пользователей из базы данных, если пользователь авторизован
    else:
        users = None
    return render_template('index.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get("login")
        password = request.form.get("password")
        if login and password:
            user = TestUser.query.filter_by(login=login).first()
            if user and check_password_hash(user.psw, password):
                login_user(user)
                next_page = request.args.get('next') or url_for('index')
                return redirect(next_page)  # Верните результат вызова функции redirect
            else:
                flash('Логин или пароль не правильный')
        else:
            flash('Ошибка авторизации')
    return render_template("login.html")  # Возвращайте шаблон по умолчанию, если не выполнено ни одно из условий


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get("login")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    if request.method == 'POST':
        if not(login or password or password2):
            flash('Заполните поля')
        elif password != password2:
            flash('Пароли не одинаковые')
        else:
            hash_psw = generate_password_hash(password)
            new_user = TestUser(login=login, psw=hash_psw)
            # сохраним нового пользователя
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# сделать возможность авторизации пользователя и после этого перенаправления на изначальную страницу
@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)

    return response






@app.route('/user_page', methods=['GET', 'POST'])
def user_page():
    pass
@app.route('/overtime_report', methods=['GET', 'POST'])
def overtime_report():
    pass
@app.route('/work_report', methods=['GET', 'POST'])
def work_report():
    pass