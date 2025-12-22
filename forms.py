from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField, FieldList, FormField, \
    SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(3, 20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class IngredientForm(FlaskForm):
    name = StringField('Ингредиент', validators=[DataRequired()])
    amount = StringField('Количество', validators=[DataRequired()])


class StepForm(FlaskForm):
    description = TextAreaField('Описание шага', validators=[DataRequired()])


class RecipeForm(FlaskForm):
    title = StringField('Название рецепта', validators=[DataRequired(), Length(1, 200)])
    description = TextAreaField('Краткое описание')
    image = FileField('Фото блюда', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    steps = FieldList(FormField(StepForm), min_entries=1)
    submit = SubmitField('Опубликовать рецепт')


class CommentForm(FlaskForm):
    text = TextAreaField('Комментарий', validators=[DataRequired(), Length(1, 1000)])
    submit = SubmitField('Отправить')


class RatingForm(FlaskForm):
    value = SelectField('Оценка', choices=[(i, f'{i} ★') for i in range(1, 6)],
                        coerce=int, validators=[DataRequired(), NumberRange(1, 5)])
    submit = SubmitField('Оценить')
