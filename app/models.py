# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)  # <-- nullable=False, но мы передаём значение
    role = Column(String, default="user")

    recipes = relationship("Recipe", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    ratings = relationship("Rating", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # НЕ NULL — теперь обязательно

    author = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    steps = relationship("Step", back_populates="recipe", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="recipe", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="recipe", cascade="all, delete-orphan")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=True)  # "200 г"
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")
class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="steps")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    author = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")

class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (UniqueConstraint("user_id", "recipe_id", name="unique_user_recipe_rating"),)

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)  # 1-5
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")