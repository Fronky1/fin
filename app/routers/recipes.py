# app/routers/recipes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, relationship

from app.database import get_db
from app.models import Recipe, Rating
from app.models import User
from app.schemas import RecipeCreate, Recipe as RecipeSchema
from app.utils import get_current_user
ratings = relationship("Rating", back_populates="recipe", cascade="all, delete-orphan")
router = APIRouter(prefix="/recipes", tags=["recipes"])

# app/routers/recipes.py (фрагмент POST)
@router.post("/", response_model=RecipeSchema, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: RecipeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        photo_url=recipe.photo_url,
        author_id=current_user.id  # <-- автоматически берём из токена!
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.get("/{recipe_id}", response_model=RecipeSchema)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    # Считаем средний рейтинг
    avg_rating = db.query(func.avg(Rating.score)).filter(Rating.recipe_id == recipe_id).scalar()
    recipe.average_rating = round(avg_rating, 1) if avg_rating else None

    return recipe

from sqlalchemy import func


@router.get("/{recipe_id}", response_model=RecipeSchema)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    # Считаем средний рейтинг
    avg_rating = db.query(func.avg(Rating.score)).filter(Rating.recipe_id == recipe_id).scalar()
    recipe.average_rating = round(avg_rating, 1) if avg_rating else None

    return recipe