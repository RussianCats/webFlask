# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, DecimalField, SelectField, SubmitField, IntegerField, HiddenField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.models import Profile, ProjectAccounting

#добавить переработки
class OvertimeReportForm(FlaskForm):
    project_name = StringField('Название проекта', validators=[DataRequired(), Length(max=255)])
    task_description = TextAreaField('Описание задачи', validators=[DataRequired()])
    task_date = StringField('Дата задачи', validators=[DataRequired()], render_kw={"class": "form-control datepicker"})
    day_type = SelectField('Тип дня', choices=[('Рабочий', 'Рабочий'),('Выходной', 'Выходной') , ('Отпускной', 'Отпускной'), ('Больничный', 'Больничный'), ('Командировочный', 'Командировочный')], validators=[DataRequired()])
    hours_worked = DecimalField('Отработанные часы', validators=[DataRequired(), NumberRange(min=0, max=24)], places=2)
    submit = SubmitField('Отправить')

class ProjectForm(FlaskForm):
    project_name = StringField('Наименование проекта', validators=[DataRequired()])
    num = StringField('Номер проекта', validators=[Optional()])
    submit = SubmitField('Добавить')

# class WorkReportForm(FlaskForm):
#     project_name = StringField('Наименование проекта', validators=[DataRequired(), Length(max=255)])
#     task_description = TextAreaField('Задача, которую выполнил', validators=[DataRequired()])
#     project_date = DateField('Дата проекта', format='%Y-%m-%d', validators=[DataRequired()])
#     hours_spent = DecimalField('Затраченное время в часах', validators=[DataRequired()], places=2)
#     submit = SubmitField('Добавить')


class WorkReportForm(FlaskForm):
    report_date = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()])
    location_work = SelectField('Выезд/офис', choices=[('Офис', 'Офис'), ('Выезд', 'Выезд')], validators=[DataRequired()])
    project_id = HiddenField('ID Проекта', validators=[DataRequired()])
    hours_spent = DecimalField('Затраченное время, ч', validators=[DataRequired(), NumberRange(min=0, max=24)], places=2)
    works = SelectField('Работы', choices=[('676', '676'), ('SDL', 'SDL'), ('SM', 'SM'), ('Атдок', 'Атдок'), ('Аттестация', 'Аттестация'),
                                            ('АУ', 'АУ'), ('Аудит', 'Аудит'), ('Категорирование', 'Категорирование'), ('Лицензирование', 'Лицензирование'),
                                            ('Оргдок', 'Оргдок'), ('ОТР', 'ОТР'), ('Пентест', 'Пентест'), ('ПНР', 'ПНР'), ('ППО', 'ППО'), ('Развитие', 'Развитие'),
                                            ('РД', 'РД'), ('САИК', 'САИК'), ('Сертдок', 'Сертдок'), ('Техдок', 'Техдок'), ('ТП', 'ТП'), ('Установка', 'Установка'),
                                            ('ЦМ', 'ЦМ')], validators=[DataRequired()])
    clarification = TextAreaField('Уточнение')
    submit = SubmitField('Отправить')