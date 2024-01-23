# auth.py
from flask import  render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Role, Profile
from app import app, manager, db
from functools import wraps


@manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# декоратор для проверки роли
def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if not any(getattr(current_user, check)() for check in roles):
                flash('У вас нет прав доступа к этой странице.')
                return redirect(url_for('index'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper





@app.route('/register', methods=['GET', 'POST'])
@login_required  
@role_required('is_admin')
def register():
    login = request.form.get("login")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    role_id = request.form.get("role")
    fio = request.form.get("fio")
    
    if request.method == 'POST':
        if not(login or password or password2 or role_id or fio):
            flash('Заполните поля')
        elif password != password2:
            flash('Пароли не одинаковые')
        else:
            dic_roles = {
                "admin": 1,
                "manager": 2,
                "employee": 3
            }
            role_id = dic_roles[f"{request.form.get('role')}"] 
            hash_psw = generate_password_hash(password)
            new_user = User(login=login, psw=hash_psw, roles_id=role_id)
            # сохраняем нового пользователя
            db.session.add(new_user)
            db.session.flush() 

            new_profile = Profile(name=fio, user_id=new_user.id)
            # сохраняем новое фио 
            db.session.add(new_profile)
            db.session.commit()
            
            return redirect(url_for('login'))

    return render_template('/auth/register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get("login")
        password = request.form.get("password")
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and check_password_hash(user.psw, password):
                login_user(user)
                next_page = request.args.get('next') or url_for('index')
                return redirect(next_page)
            else:
                flash('Логин или пароль не правильный')
        else:
            flash('Ошибка авторизации')
    return render_template("/auth/login.html")






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
