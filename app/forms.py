# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class OvertimeReportForm(FlaskForm):
    project_name = StringField('Название проекта', validators=[DataRequired(), Length(max=255)])
    task_description = TextAreaField('Описание задачи', validators=[DataRequired()])
    task_date = StringField('Дата задачи', validators=[DataRequired()], render_kw={"class": "form-control datepicker"})
    day_type = SelectField('Тип дня', choices=[('Рабочий', 'Рабочий'),('Выходной', 'Выходной') , ('Отпускной', 'Отпускной'), ('Больничный', 'Больничный'), ('Командировочный', 'Командировочный')], validators=[DataRequired()])
    hours_worked = DecimalField('Отработанные часы', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Отправить')
