# app/schemas.py
from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    # Можно добавить время приготовления, сложность и т.д.

class RecipeCreate(RecipeBase):
    # Здесь можно добавить списки ингредиентов и шагов, если реализуешь их позже
    pass

class Recipe(RecipeBase):
    id: int
    author_id: Optional[int] = None  # будет после аутентификации

    class Config:
        from_attributes = True  # Важно! Позволяет конвертировать SQLAlchemy-модели в Pydantic

# app/schemas.py (добавь в конец)
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CommentCreate(BaseModel):
    text: str
    recipe_id: int

class Comment(CommentCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    score: int  # 1-5
    recipe_id: int

class Rating(RatingCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# app/schemas.py — добавь в конец
class RatingCreate(BaseModel):
    score: int  # 1-5
    recipe_id: int

class Rating(RatingCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
# app/schemas.py — добавь в конец
class RatingCreate(BaseModel):
    score: int  # 1-5
    recipe_id: int

class Rating(RatingCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Для рецепта с рейтингом (опционально, если хочешь отдельную схему)
class RecipeWithRating(Recipe):
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None

    class Config:
        from_attributes = True
