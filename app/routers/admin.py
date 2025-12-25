# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Recipe, User
from app.schemas import Recipe as RecipeSchema
from app.utils import get_current_admin
from typing import List

router = APIRouter(prefix="/admin", tags=["Админ-панель"])

@router.get("/recipes", response_model=List[RecipeSchema])
def get_all_recipes(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(Recipe).all()

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    db.delete(recipe)
    db.commit()
    return {"message": "Рецепт удалён"}

@router.get("/users")
def get_all_users(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(User).all()