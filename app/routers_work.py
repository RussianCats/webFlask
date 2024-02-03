from flask import  render_template, redirect, flash, url_for, send_file, request, jsonify
from app import app, db
from app.models import User, OvertimeReport, Profile, ProjectAccounting, ProjectReports
from app.auth import role_required, login_required, current_user
from app.forms import  ProjectForm, WorkReportForm
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
        user_profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not user_profile:
            flash('Профиль пользователя не найден.', 'warning')
            return redirect(url_for('work_report_add_action'))

        new_report = ProjectReports(
            project_id=form.project_id.data,
            profiles_id=user_profile.id,
            report_date=form.report_date.data,
            location_work=form.location_work.data,
            hours_spent=form.hours_spent.data,
            works=form.works.data,
            clarification=form.clarification.data
        )
        try:
            db.session.add(new_report)
            db.session.commit()
            flash('Отчет успешно добавлен!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка добавления отчета: {str(e)}', 'error')
        return redirect(url_for('work_report_add_action'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}", 'error')

    return render_template('work_report/add_action.html', title='Добавить рабочий отчет', form=form)


# для поиска проектов в поле 
@app.route('/work_report/search-projects')
def search_projects():
    query = request.args.get('query', '', type=str)
    projects = ProjectAccounting.query.filter(ProjectAccounting.project_name.ilike(f'%{query}%')).all()
    projects_data = [{'id': project.id, 'name': project.project_name} for project in projects]
    return jsonify({'projects': projects_data})

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def work_report_add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = ProjectAccounting(project_name=form.project_name.data, num=form.num.data)
        db.session.add(project)
        db.session.commit()
        flash('Проект успешно добавлен!')
        return redirect(url_for('work_report'))  # Перенаправьте пользователя куда-либо после добавления проекта

    return render_template('work_report/add_project_action.html', form=form)


@app.route('/work_report/unload_action', methods=['GET', 'POST'])
def work_report_unload_action():
    return render_template('work_report/work_report.html')

