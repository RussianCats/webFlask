from flask import  render_template, redirect, flash, url_for
from app import app, db
from app.models import User, OvertimeReport
from app.auth import role_required, login_required, current_user
from app.forms import OvertimeReportForm




@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')






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





# маршуты для переработок
@app.route('/work_report', methods=['GET', 'POST'])
def work_report():
    return render_template('work_report.html')

# просмотр пререаботок пользователя
@app.route('/overwork/view_action', methods=['GET', 'POST'])
@login_required
def view_action():
    # Извлечение записей из таблицы overtime_report только для текущего пользователя
    reports = OvertimeReport.query.filter_by(user_id=current_user.id).all()
    return render_template('overwork/view_action.html', reports=reports)

# удаление записей в бд для /overwork/view_action
@app.route('/overwork/delete_action/<int:report_id>', methods=['POST'])
@login_required
def delete_action(report_id):
    report = OvertimeReport.query.get_or_404(report_id)
    # Проверка, что текущий пользователь является владельцем записи
    if report.user_id != current_user.id:
        flash('Нет прав для удаления этой записи.', 'danger')
        return redirect(url_for('view_action'))
    db.session.delete(report)
    db.session.commit()
    flash('Запись успешно удалена.', 'success')
    return redirect(url_for('view_action'))

@app.route('/overwork/add_action', methods=['GET', 'POST'])
@login_required
def add_action():
    form = OvertimeReportForm()
    if form.validate_on_submit():
        report = OvertimeReport(
            project_name=form.project_name.data,
            task_description=form.task_description.data,
            task_date=form.task_date.data,
            day_type=form.day_type.data,
            hours_worked=form.hours_worked.data,
            user_id=current_user.id  # Предполагается, что у вас есть аутентификация
        )
        db.session.add(report)
        db.session.commit()
        flash('Overtime report has been added.', 'success')
        return redirect(url_for('add_action'))  # Перенаправление на главную страницу или другую страницу

    return render_template('/overwork/add_action.html', title='Add Overtime Report', form=form)


@app.route('/overwork/upload_action', methods=['GET', 'POST'])
def upload_action():
    return render_template('overwork/upload_action.html')