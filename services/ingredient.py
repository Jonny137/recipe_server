from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.ingredient import Ingredient
from core.exceptions import RecipeServerException
from schemas.ingredient import Ingredient as IngredientSchema


def create_new_ingredient(
        ingredient_name: str, db: Session
) -> IngredientSchema:
    try:
        new_ingredient = Ingredient(name=ingredient_name)

        db.add(new_ingredient)
        db.commit()

        return new_ingredient
    except IntegrityError:
        raise RecipeServerException(
            status_code=400, message='Duplicated entry.'
        )


def get_most_used_ingredients(db: Session) -> Optional[IngredientSchema]:
    return (
        db.query(Ingredient)
        .join(Ingredient.recipes)
        .group_by(Ingredient.id)
        .order_by(func.count().desc()).limit(5).all()
    )
