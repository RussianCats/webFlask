from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from userLogin import UserLogin

app = Flask(__name__)

# Настройка подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5892@localhost:5432/web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Данная функция заносит в сессию информацию о зарегистрированном пользователе, используя определенные в классе методы. 
# После этого сессионная информация будет присутствовать во всех запросах к серверу. Для ее обработки во Flask-Login определен специальный декоратор: 
@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

# Определение модели Role
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    label = db.Column(db.Text, nullable=False)

    # Связь с моделью User
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f'<Role {self.label}>'

# Определение модели User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)  
    fio = db.Column(db.Text, nullable=False)
    id_role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_blocked = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.login}>'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/auth')
def auth():
    return render_template("auth.html")

@app.route('/reports')
def reports():
    return render_template("report.html")

@app.route('/test')
def test():
    users = User.query.all()  # Извлечение всех пользователей из базы данных
    return render_template("test.html", users=users)


# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     user = User.query.get(id)
#     if user and user.name == name:
#         return 'User page ' + str(name) + "-" + str(id)
#     else:
#         return 'User not found', 404

if __name__ == '__main__':
    app.run(debug=True)
