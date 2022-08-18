from email.policy import default
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, RadioField
from wtforms.validators import DataRequired, NumberRange


class Movement(FlaskForm):

    direction = SelectField(
        "В какую сторону вы отправитесь? ",
        validators = [DataRequired()],
        choices = [
            'Север', 'Восток', 'Юг', 'Запад'
            ],
        render_kw = {
            'class': 'form-control'	
        }
    )
    distance = IntegerField(
        "Насколько далеко вы зайдете",
        validators = [NumberRange(1, 20)],
        render_kw = {
            'class': 'form-control'	
        },
        default=1
    )
    
    submit = SubmitField("Submit", render_kw={
            'class': 'form-control'
        }
    )

class Preferences(FlaskForm):

    control_type = RadioField(
        'Выберите тип управления',
        coerce = int,
        choices = [
            (0, 'Классик (как в описании к заданию)'),
            (1, 'Стрелки (поддерживаеся ввод с клавиатуры)')
            ],
        render_kw={
            'class': 'form-check'	
        },
        default=0
    )
    generation_type = RadioField(
        'Выберите тип генерации',
        coerce = int,
        choices = [
            (0, 'Селф мейд случайные стены'),
            (1, 'Генератор Лабиринта')
            ],
        render_kw={
            'class': 'form-check',
        },
        default=0
    )
    height = IntegerField(
        "Высота поля",
        validators = [NumberRange(3, 10)],
        render_kw = {
            'class': 'form-control'	
        },
        default=4
    )
    width = IntegerField(
        "Ширина поля",
        validators = [NumberRange(3, 10)],
        render_kw = {
            'class': 'form-control'	
        },
        default=6
    )
    submit = SubmitField("Submit", render_kw={
            'class': 'form-control'
        }
    )