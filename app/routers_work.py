from flask import  render_template, redirect, flash, url_for, send_file, request
from app import app, db
from app.models import User, OvertimeReport, Profile, ProjectAccounting, WorkReport
from app.auth import role_required, login_required, current_user
from app.forms import WorkReportForm, ProjectForm
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO
from datetime import datetime
from sqlalchemy import desc


@app.route('/work_report')
def work_report():
    return render_template('work_report/work_report.html')


@app.route('/work_report/view_action', methods=['GET', 'POST'])
def work_report_view_action():
    return render_template('work_report/work_report.html')

@app.route('/work_report/add_action', methods=['GET', 'POST'])
@login_required
def work_report_add_action():
    form = WorkReportForm()
    if form.validate_on_submit():
        # Сначала добавляем запись в ProjectAccounting
        project = ProjectAccounting(project_name=form.project_name.data)
        db.session.add(project)
        db.session.flush()  # flush для получения id добавленного проекта, необходимо для ссылки в WorkReport

        # Теперь добавляем запись в WorkReport
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        work_report = WorkReport(
            project_id=project.id,
            profiles_id=profile.id,
            project_date=form.project_date.data,
            task_performed=form.task_description.data,
            hours_spent=form.hours_spent.data
        )
        db.session.add(work_report)
        db.session.commit()
        flash('Рабочий отчет успешно добавлен!', 'success')
        return redirect(url_for('work_report'))

    return render_template('work_report/add_action.html', title='Добавить рабочий отчет', form=form)


@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def work_report_add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = ProjectAccounting(project_name=form.project_name.data)
        db.session.add(project)
        db.session.commit()
        flash('Проект успешно добавлен!')
        return redirect(url_for('work_report'))  # Перенаправьте пользователя куда-либо после добавления проекта

    return render_template('work_report/add_project_action.html', form=form)

@app.route('/work_report/unload_action', methods=['GET', 'POST'])
def work_report_unload_action():
    return render_template('work_report/work_report.html')

