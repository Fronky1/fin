# app/routers/ratings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Rating, Recipe, User
from app.schemas import RatingCreate, Rating as RatingSchema
from app.utils import get_current_user

router = APIRouter(prefix="/ratings", tags=["Рейтинги"])

@router.post("/", response_model=RatingSchema, status_code=status.HTTP_201_CREATED)
def create_or_update_rating(
    rating_in: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверка рецепта
    recipe = db.query(Recipe).filter(Recipe.id == rating_in.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    # Проверка диапазона
    if not 1 <= rating_in.score <= 5:
        raise HTTPException(status_code=400, detail="Рейтинг должен быть от 1 до 5")

    # рейтинг
    existing = db.query(Rating).filter(
        Rating.recipe_id == rating_in.recipe_id,
        Rating.user_id == current_user.id
    ).first()

    if existing:
        existing.score = rating_in.score
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_rating = Rating(
            score=rating_in.score,
            recipe_id=rating_in.recipe_id,
            user_id=current_user.id
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating