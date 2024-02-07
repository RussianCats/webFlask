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
@login_required
def work_report_view_action():
    # Получаем профиль текущего пользователя
    page = request.args.get('page', 1, type=int)  # Получаем номер текущей страницы из запроса

    # Получаем профиль текущего пользователя
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash('Профиль пользователя не найден.', 'warning')
        return redirect(url_for('index'))

    # Изменяем запрос, добавляем пагинацию
    reports_pagination = db.session.query(
        ProjectReports,
        ProjectAccounting.project_name,
        ProjectAccounting.num
    ).join(
        ProjectAccounting, ProjectReports.project_id == ProjectAccounting.id
    ).filter(
        ProjectReports.profiles_id == profile.id
    ).paginate(page=page, per_page=30, error_out=False)  
    return render_template('work_report/view_action.html', reports=reports_pagination.items, pagination=reports_pagination)



# удаление записей в бд для /work_report/view_action
@app.route('/work_report/delete_action/<int:report_id>', methods=['POST'])
@login_required
def work_report_delete_action(report_id):
    # Получаем запись из ProjectReports, а не из OvertimeReport
    report = ProjectReports.query.get_or_404(report_id)

    # Получаем профиль текущего пользователя
    user_profile = Profile.query.filter_by(user_id=current_user.id).first()

    # Проверяем, соответствует ли profiles_id в отчете ID профиля текущего пользователя
    if not user_profile or report.profiles_id != user_profile.id:
        flash('Нет прав для удаления этой записи.', 'danger')
        return redirect(url_for('work_report_view_action'))

    db.session.delete(report)
    db.session.commit()
    flash('Запись успешно удалена.', 'success')
    return redirect(url_for('work_report_view_action'))



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
@login_required
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

# форматирование ФИО
def format_name(full_name):
    parts = full_name.split()  # Разделение строки по пробелу
    if len(parts) >= 3:
        # Если есть имя, отчество и фамилия, форматируем в "Фамилия И.О."
        return f"{parts[0]} {parts[1][0]}.{parts[2][0]}."

    return full_name  # Возвращаем исходное имя, если не подходит под условия


@app.route('/work_report/unload_action', methods=['GET', 'POST'])
@login_required
@role_required('is_admin', 'is_manager')
def work_report_unload_action():
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        # Попытка преобразования даты и проверка введенных данных
        try:
            start_date = datetime.strptime(start_date_str, '%d.%m.%Y').date()
            end_date = datetime.strptime(end_date_str, '%d.%m.%Y').date()
        except ValueError:
            # В случае ошибки возвращаем пользователя на форму с сообщением об ошибке
            flash('Неверный формат даты. Пожалуйста, используйте формат дд.мм.гггг', 'error')
            return redirect(url_for('unload_action'))  # Вернуться к форме

        if start_date > end_date:
            flash('Начальная дата не может быть позже конечной даты.', 'error')
            return redirect(url_for('work_report_unload_action'))
        # Здесь логика обработки и создания отчета...

        # Получение данных из БД
        reports = db.session.query(
            ProjectReports,
            Profile.name,
            ProjectAccounting.project_name,
            ProjectAccounting.num
        ).join(
            Profile, ProjectReports.profiles_id == Profile.id
        ).join(
            ProjectAccounting, ProjectReports.project_id == ProjectAccounting.id
        ).filter(
            ProjectReports.report_date >= start_date,
            ProjectReports.report_date <= end_date
        ).order_by(Profile.name, ProjectReports.report_date).all()

        

        # Создание рабочей книги и листа
        wb = Workbook()
        ws = wb.active
        ws.title = "Overwork Reports"

        # Заголовки для файла Excel
        columns = [
             'ФИО', 'Дата', 'Выезд/офис', 'Проект',
            'Номер задачи', 'Затраченное время, ч', 'Работы', 'Уточнение'
        ]

        # Добавление заголовков в лист
        ws.append(columns)

        # Добавление данных в лист
        for report, profile_name, project_name, num in reports:
            formatted_name = format_name(profile_name)  # Форматирование имени
            row = [
                formatted_name,  # Использование отформатированного имени
                report.report_date.strftime('%d.%m.%Y'),
                report.location_work,
                project_name,
                num,
                report.hours_spent,
                report.works,
                report.clarification
            ]
            ws.append(row)

        # Сохранение файла Excel в памяти
        virtual_workbook = BytesIO()
        wb.save(virtual_workbook)
        virtual_workbook.seek(0)

        # Отправка файла пользователю
        return send_file(virtual_workbook, as_attachment=True, download_name='отчет по отделу.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        

    # Если это GET запрос, просто отображаем форму
    return render_template('work_report/unload_action.html')

