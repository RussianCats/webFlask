# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, DecimalField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models import Profile, ProjectAccounting

#добавить переработки
class OvertimeReportForm(FlaskForm):
    project_name = StringField('Название проекта', validators=[DataRequired(), Length(max=255)])
    task_description = TextAreaField('Описание задачи', validators=[DataRequired()])
    task_date = StringField('Дата задачи', validators=[DataRequired()], render_kw={"class": "form-control datepicker"})
    day_type = SelectField('Тип дня', choices=[('Рабочий', 'Рабочий'),('Выходной', 'Выходной') , ('Отпускной', 'Отпускной'), ('Больничный', 'Больничный'), ('Командировочный', 'Командировочный')], validators=[DataRequired()])
    hours_worked = DecimalField('Отработанные часы', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Отправить')

# для добавления наименования
class ProjectForm(FlaskForm):
    project_name = StringField('Наименование проекта', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class WorkReportForm(FlaskForm):
    project_name = StringField('Наименование проекта', validators=[DataRequired(), Length(max=255)])
    task_description = TextAreaField('Задача, которую выполнил', validators=[DataRequired()])
    project_date = DateField('Дата проекта', format='%Y-%m-%d', validators=[DataRequired()])
    hours_spent = DecimalField('Затраченное время в часах', validators=[DataRequired()], places=2)
    submit = SubmitField('Добавить')