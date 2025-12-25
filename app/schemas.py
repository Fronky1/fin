from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    photo_url: Optional[str] = None

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    created_at: datetime
    author_id: int
    average_rating: Optional[float] = None  #средний рейтинг

    class Config:
        from_attributes = True

RecipeSchema = Recipe

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