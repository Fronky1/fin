from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db

with app.app_context():
    db.create_all()
from models import User, Recipe, Ingredient, Step, Comment, Rating
from forms import RegistrationForm, LoginForm, RecipeForm, CommentForm, RatingForm
from utils import save_picture


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('index.html', recipes=recipes)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Аккаунт создан! Теперь можно войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            author=current_user
        )
        if form.image.data:
            recipe.image = save_picture(form.image.data)

        for ing_form in form.ingredients.data:
            ing = Ingredient(name=ing_form['name'], amount=ing_form['amount'], recipe=recipe)
            db.session.add(ing)

        for i, step_form in enumerate(form.steps.data, 1):
            step = Step(number=i, description=step_form['description'], recipe=recipe)
            db.session.add(step)

        db.session.add(recipe)
        db.session.commit()
        flash('Рецепт опубликован!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe.id))
    return render_template('add_recipe.html', form=form)

@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    comment_form = CommentForm()
    rating_form = RatingForm()

    # текущая оценка пользователя
    user_rating = None
    if current_user.is_authenticated:
        user_rating = Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()

    if user_rating:
        rating_form.value.data = user_rating.value

    return render_template('recipe_detail.html', recipe=recipe,
                           comment_form=comment_form, rating_form=rating_form,
                           user_rating=user_rating)

@app.route("/recipe/<int:recipe_id>/comment", methods=['POST'])
@login_required
def add_comment(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, author=current_user, recipe=recipe)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен', 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route("/recipe/<int:recipe_id>/rate", methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RatingForm()
    if form.validate_on_submit():
        rating = Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()
        if rating:
            rating.value = form.value.data
        else:
            rating = Rating(value=form.value.data, user=current_user, recipe=recipe)
            db.session.add(rating)
        db.session.commit()
        flash('Спасибо за оценку!', 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route("/search")
def search():
    query = request.args.get('q', '').strip()
    ingredient = request.args.get('ing', '').strip()

    recipes = Recipe.query

    if query:
        recipes = recipes.filter(Recipe.title.ilike(f'%{query}%'))
    if ingredient:
        recipes = recipes.join(Ingredient).filter(Ingredient.name.ilike(f'%{ingredient}%'))

    recipes = recipes.order_by(Recipe.created_at.desc()).all()
    return render_template('search.html', recipes=recipes, query=query, ingredient=ingredient)