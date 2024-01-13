from crypt import methods
from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass









@app.route('/user_page', methods=['GET', 'POST'])
def user_page():
    pass
@app.route('/overtime_report', methods=['GET', 'POST'])
def overtime_report():
    pass
@app.route('/work_report', methods=['GET', 'POST'])
def work_report():
    pass