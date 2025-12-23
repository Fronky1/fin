# app/routers/comments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Comment, Recipe, User
from app.schemas import CommentCreate, Comment as CommentSchema
from app.utils import get_current_user

router = APIRouter(prefix="/comments", tags=["Комментарии"])


@router.post("/", response_model=CommentSchema)
def create_comment(
        comment: CommentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Проверка существования рецепта
    recipe = db.query(Recipe).filter(Recipe.id == comment.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    new_comment = Comment(
        text=comment.text,
        recipe_id=comment.recipe_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/recipe/{recipe_id}", response_model=List[CommentSchema])
def get_comments_for_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.recipe_id == recipe_id).all()