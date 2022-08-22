import logging
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.ingredient import Ingredient
from core.exceptions import RecipeServerException
from schemas.ingredient import Ingredient as IngredientSchema


logger = logging.getLogger(__name__)


def create_new_ingredient(
        ingredient_name: str, db: Session
) -> IngredientSchema:
    try:
        new_ingredient = Ingredient(name=ingredient_name)

        db.add(new_ingredient)
        db.commit()

        logger.info(
            f'Successfully added new ingredient with name: {ingredient_name}'
        )
        return new_ingredient
    except IntegrityError:
        logger.error(f'Error ingredient creation with name: {ingredient_name}')
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
