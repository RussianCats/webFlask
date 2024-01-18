from flask import  render_template, request, flash, url_for
from app import app, manager, db
from app.models import User
from app.auth import role_required, login_required
from flask_login import current_user 





@app.route('/index')
@app.route('/')
def index():
    if current_user.is_authenticated:
        users = User.query.all()  # Получаем всех пользователей из базы данных, если пользователь авторизован
    else:
        users = None
    return render_template('index.html', users=users)






@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required  
@role_required('is_admin')
def admin_panel():
    return render_template('index.html')

@app.route('/user_page', methods=['GET', 'POST'])
def user_page():
    return render_template('index.html')

@app.route('/overtime_report', methods=['GET', 'POST'])
def overtime_report():
    return render_template('overtime_report.html')

@app.route('/work_report', methods=['GET', 'POST'])
def work_report():
    return render_template('work_report.html')