
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from uuid import uuid4
import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Recipe, User, RecipeIngredient, Rating
from app.schemas import RecipeCreate, Recipe as RecipeSchema
from app.utils import get_current_user

router = APIRouter(prefix="/recipes", tags=["recipes"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=RecipeSchema, status_code=status.HTTP_201_CREATED)
async def create_recipe(
        title: str = Form(...),
        description: Optional[str] = Form(None),
        photo: Optional[UploadFile] = File(None),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    photo_url = None
    if photo:
        suffix = photo.filename.split(".")[-1] if "." in photo.filename else "jpg"
        filename = f"{uuid4()}.{suffix}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            content = await photo.read()
            buffer.write(content)

        photo_url = f"/static/uploads/{filename}"

    db_recipe = Recipe(
        title=title,
        description=description,
        photo_url=photo_url,
        author_id=current_user.id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.get("/", response_model=List[RecipeSchema])
def read_recipes(
        q: Optional[str] = None,  # поиск по названию
        ingredient: Optional[str] = None,  # поиск по ингредиентам
        db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if q:
        query = query.filter(Recipe.title.ilike(f"%{q}%"))

    if ingredient:
        query = query.join(RecipeIngredient).filter(RecipeIngredient.name.ilike(f"%{ingredient}%"))

    recipes = query.all()

    for recipe in recipes:
        avg_rating = db.query(func.avg(Rating.score)).filter(Rating.recipe_id == recipe.id).scalar()
        recipe.average_rating = round(avg_rating, 1) if avg_rating else None

    return recipes


@router.get("/{recipe_id}", response_model=RecipeSchema)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    # Средний рейтинг
    avg_rating = db.query(func.avg(Rating.score)).filter(Rating.recipe_id == recipe_id).scalar()
    recipe.average_rating = round(avg_rating, 1) if avg_rating else None

    return recipe


@router.get("/", response_model=List[RecipeSchema])
def read_recipes(
        q: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Recipe)
    if q:
        query = query.filter(Recipe.title.ilike(f"%{q}%") | RecipeIngredient.name.ilike(f"%{q}%"))
    return query.all()
